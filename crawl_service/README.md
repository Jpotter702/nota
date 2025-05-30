# Crawl Service

The Crawl Service is responsible for extracting content from websites using the `crawl4ai` library. It provides a flexible interface for configuring crawl jobs and supports various output formats and processing modes.

## Features

- **Configurable Crawl Depth**: Control how deep the crawler should navigate from the starting URL
- **Domain Restrictions**: Option to include or exclude subdomains
- **Robots.txt Compliance**: Respect website crawling policies
- **Multiple Output Formats**: Generate content in markdown, HTML, or JSON
- **Content Filtering**: Clean and filter content to remove noise
- **AI-Powered Extraction**: Extract specific information or generate summaries

## Usage

### Command Line Interface

Run the crawl service with interactive prompts:

```bash
python crawl_service/main.py
```

Run with a configuration file:

```bash
python crawl_service/main.py --config crawl_service/config/job.yaml
```

### Configuration File Format

Create a YAML configuration file with the following structure:

```yaml
url: https://example.com
max_depth: 2
include_subdomains: false
obey_robots_txt: true
bypass_cache: true
mode: markdown-fit  # Optional: applies mode-specific settings
```

### Available Modes

The crawl service supports the following modes:

1. **markdown**: Basic markdown output
2. **markdown-fit**: Filtered and cleaned markdown output
3. **html**: Basic HTML output
4. **html-fit**: Filtered and cleaned HTML output
5. **summary (json_extract)**: AI-generated summaries of content
6. **schema**: Extract structured data based on a schema
7. **filter_config**: Apply custom filtering rules

## Output

Crawl results are saved to `crawl_service/output/results.json` by default. The output contains an array of page objects with the following structure:

```json
[
  {
    "url": "https://example.com",
    "title": "Example Domain",
    "content": "...",
    "markdown": "...",
    "html": "..."
  }
]
```

## Integration

The Crawl Service is designed to work with the Render Service, which can process the output JSON into various formats for presentation or further processing.

## Dependencies

- crawl4ai: Web crawling engine
- pydantic: Data validation
- yaml: Configuration file parsing 