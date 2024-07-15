# Web Content Analysis Tool

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
