import ollama
import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import configparser
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Load configuration
config = configparser.ConfigParser()
config_file = 'config.ini'

if not os.path.exists(config_file):
    config['DEFAULT'] = {
        'MODEL': 'llama2',
        'CACHE_DIR': 'content_cache',
        'ANALYSIS_CACHE_DIR': 'analysis_cache',
        'MAX_CONTENT_SIZE': '1000000'
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

config.read(config_file)

MODEL = config['DEFAULT']['MODEL']
CACHE_DIR = config['DEFAULT']['CACHE_DIR']
ANALYSIS_CACHE_DIR = config['DEFAULT']['ANALYSIS_CACHE_DIR']
MAX_CONTENT_SIZE = int(config['DEFAULT']['MAX_CONTENT_SIZE'])

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(ANALYSIS_CACHE_DIR, exist_ok=True)

class WebContentAnalyzer:
    def __init__(self, model=MODEL):
        self.model = model

    def fetch_content(self, url):
        """Fetch content from a given URL, with caching and size limit."""
        cache_file = os.path.join(CACHE_DIR, self._url_to_filename(url))
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return json.load(f)["content"]

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            
            if content:
                text_content = content.get_text(separator='\n', strip=True)
            else:
                text_content = soup.get_text(separator='\n', strip=True)
            
            if len(text_content) > MAX_CONTENT_SIZE:
                text_content = text_content[:MAX_CONTENT_SIZE] + "... (content truncated)"

            with open(cache_file, "w") as f:
                json.dump({"url": url, "content": text_content}, f)

            return text_content
        except requests.RequestException as e:
            logging.error(f"Error fetching content from {url}: {str(e)}")
            return None

    def _url_to_filename(self, url):
        """Convert URL to a valid filename for caching."""
        return urlparse(url).netloc + urlparse(url).path.replace("/", "_") + ".json"

    def query_ollama(self, messages):
        """Query the Ollama model with given messages."""
        try:
            response = ollama.chat(model=self.model, messages=messages)
            return response['message']['content']
        except Exception as e:
            logging.error(f"Error querying Ollama: {str(e)}")
            return None

    def analyze_content(self, content, analysis_type):
        """Analyze content based on the specified analysis type, with caching."""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        cache_file = os.path.join(ANALYSIS_CACHE_DIR, f"{analysis_type}_{content_hash}.json")
        
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return json.load(f)["result"]

        prompts = {
            'summarize': f"Provide a concise summary of the following text:\n\n{content[:1000]}...",
            'keywords': f"Extract and list the 5-10 most important keywords or key phrases from the following text:\n\n{content[:1000]}...",
            'sentiment': f"Analyze the overall sentiment of the following text. Classify it as positive, negative, or neutral, and provide a brief explanation:\n\n{content[:1000]}...",
        }
        
        if analysis_type in prompts:
            result = self.query_ollama([{"role": "user", "content": prompts[analysis_type]}])
            if result:
                with open(cache_file, "w") as f:
                    json.dump({"content_hash": content_hash, "result": result}, f)
            return result
        else:
            return None

    def compare_urls(self, urls):
        """Compare content from multiple URLs."""
        contents = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.fetch_content, url): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    content = future.result()
                    if content:
                        contents[url] = content
                except Exception as e:
                    logging.error(f"Error fetching {url}: {str(e)}")
        
        if not contents:
            return "Failed to fetch content from any of the provided URLs."
        
        comparison_prompt = "Compare and contrast the following web pages:\n\n"
        for url, content in contents.items():
            comparison_prompt += f"URL: {url}\nContent: {content[:500]}...\n\n"
        comparison_prompt += "Provide a detailed comparison focusing on similarities, differences, and unique aspects of each page."
        
        return self.query_ollama([{"role": "user", "content": comparison_prompt}])

class Command:
    def execute(self, analyzer, content):
        pass

class FetchContent(Command):
    def execute(self, analyzer, content):
        url = input("Enter a URL to fetch content: ").strip()
        print("Fetching content...")
        content = analyzer.fetch_content(url)
        if content:
            print("\nContent fetched. You can now choose an analysis option.")
        else:
            print("\nFailed to fetch content. Please try again or enter a different URL.")
        return content

class AnalyzeContent(Command):
    def __init__(self, analysis_type):
        self.analysis_type = analysis_type

    def execute(self, analyzer, content):
        if not content:
            print("Please fetch content first by entering a URL.")
            return content

        print(f"\nPerforming {self.analysis_type} analysis...")
        result = analyzer.analyze_content(content, self.analysis_type)
        if result:
            print(f"\nAnalysis Result: {result}")
        else:
            print("\nAnalysis failed. Please try again.")
        return content

class CompareURLs(Command):
    def execute(self, analyzer, content):
        urls = []
        while True:
            url = input("Enter a URL to compare (or press Enter to finish): ").strip()
            if not url:
                break
            urls.append(url)
        
        if len(urls) < 2:
            print("Please enter at least two URLs for comparison.")
            return content
        
        print("\nComparing URLs...")
        comparison = analyzer.compare_urls(urls)
        if comparison:
            print(f"\nComparison Result: {comparison}")
        else:
            print("\nComparison failed. Please try again.")
        return content

class CustomQuery(Command):
    def execute(self, analyzer, content):
        if not content:
            print("Please fetch content first by entering a URL.")
            return content
        
        query = input("\nEnter your custom query about the content: ")
        print("Processing your query...")
        response = analyzer.query_ollama([{"role": "user", "content": f"Based on the following content, {query}\n\nContent: {content[:1000]}..."}])
        if response:
            print(f"\nOllama: {response}")
        else:
            print("\nQuery failed. Please try again.")
        return content

def get_user_choice():
    print("\nChoose an option:")
    print("1. Fetch Content")
    print("2. Summarize")
    print("3. Extract Keywords")
    print("4. Analyze Sentiment")
    print("5. Compare URLs")
    print("6. Custom Query")
    print("7. Quit")
    return input("\nYour choice: ").strip()

def main():
    analyzer = WebContentAnalyzer()
    content = ""
    commands = {
        '1': FetchContent(),
        '2': AnalyzeContent('summarize'),
        '3': AnalyzeContent('keywords'),
        '4': AnalyzeContent('sentiment'),
        '5': CompareURLs(),
        '6': CustomQuery()
    }

    print("Welcome to the Enhanced Ollama Web Content Analysis Tool!")
    print("This tool allows you to analyze and compare web content using Ollama models.")
    print(f"Current configuration: Model={MODEL}, Max Content Size={MAX_CONTENT_SIZE} bytes")

    while True:
        choice = get_user_choice()
        
        if choice == '7':
            print("Thank you for using the Web Content Analysis Tool. Goodbye!")
            break

        command = commands.get(choice)
        if command:
            content = command.execute(analyzer, content)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
