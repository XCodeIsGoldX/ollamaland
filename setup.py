import os
import shutil

def create_directory_structure():
    # Create main directory
    os.makedirs("web-content-analyzer", exist_ok=True)
    os.chdir("web-content-analyzer")

    # Create subdirectories
    os.makedirs("tests", exist_ok=True)

    # Create .gitignore
    with open(".gitignore", "w") as f:
        f.write("""__pycache__/
*.py[cod]
*$py.class
*.so
.env
.venv
env/
venv/
ENV/
content_cache/
analysis_cache/
*.log
""")

    # Create LICENSE
    with open("LICENSE", "w") as f:
        f.write("""MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

    # Create README.md
    with open("README.md", "w") as f:
        f.write("""# Web Content Analysis Tool

This tool allows users to fetch, analyze, and compare web content using Ollama models. It provides features such as content summarization, keyword extraction, sentiment analysis, and URL comparison.

## Features

- Fetch and cache web content
- Analyze content using various methods (summarize, extract keywords, analyze sentiment)
- Compare multiple URLs
- Configurable settings via a config file
- Result caching for improved performance

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/web-content-analyzer.git
   cd web-content-analyzer
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up Ollama:
   Ensure you have Ollama installed and running on your system. Follow the installation instructions on the [Ollama GitHub page](https://github.com/ollama/ollama).

## Configuration

Edit the `config.ini` file to customize settings:

- `MODEL`: The Ollama model to use for analysis (default: 'llama2')
- `CACHE_DIR`: Directory to store cached web content (default: 'content_cache')
- `ANALYSIS_CACHE_DIR`: Directory to store cached analysis results (default: 'analysis_cache')
- `MAX_CONTENT_SIZE`: Maximum size of content to fetch and analyze, in bytes (default: 1000000)

## Usage

Run the script using Python:

```
python web_content_analyzer.py
```

Follow the on-screen prompts to use various features of the tool.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
""")

    # Create requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("""ollama==0.1.0
requests==2.26.0
beautifulsoup4==4.10.0
python-dotenv==0.19.1
tqdm==4.62.3
""")

    # Create config.ini
    with open("config.ini", "w") as f:
        f.write("""[DEFAULT]
MODEL = llama2
CACHE_DIR = content_cache
ANALYSIS_CACHE_DIR = analysis_cache
MAX_CONTENT_SIZE = 1000000
""")

    # Create web_content_analyzer.py
    # Note: You should replace this with your actual script content
    with open("web_content_analyzer.py", "w") as f:
        f.write("""# Your web_content_analyzer.py script goes here
""")

    # Create tests/test_web_content_analyzer.py
    with open("tests/test_web_content_analyzer.py", "w") as f:
        f.write("""import unittest
from web_content_analyzer import WebContentAnalyzer

class TestWebContentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = WebContentAnalyzer()

    def test_fetch_content(self):
        # Add test for fetch_content method
        pass

    def test_analyze_content(self):
        # Add test for analyze_content method
        pass

    def test_compare_urls(self):
        # Add test for compare_urls method
        pass

if __name__ == '__main__':
    unittest.main()
""")

def main():
    create_directory_structure()
    print("Project structure created successfully!")
    print("Next steps:")
    print("1. Replace the content of web_content_analyzer.py with your actual script.")
    print("2. Review and update the README.md file as needed.")
    print("3. Update the LICENSE file with your name or organization.")
    print("4. Initialize a git repository and push to GitHub:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git remote add origin https://github.com/yourusername/web-content-analyzer.git")
    print("   git push -u origin main")

if __name__ == "__main__":
    main()
