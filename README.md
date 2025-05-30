# Nota - Web Content Processing System

Nota is a modular web content processing system designed to crawl websites, render the content in various formats, and export the results to different file types.

## Architecture

The system consists of three main services:

1. **Crawl Service**: Crawls websites and extracts content using various strategies
2. **Render Service**: Processes the crawled data into readable formats
3. **Export Service**: Converts rendered content to final output formats (PDF, DOCX, TXT)

## Services

### Crawl Service

Handles web crawling using the `crawl4ai` library. Features include:
- Configurable crawl depth and domain restrictions
- Multiple output formats (markdown, HTML, JSON)
- Content filtering and cleaning
- Schema-based extraction
- AI-powered summarization

### Render Service

Processes crawled data into readable formats:
- Renders content as Markdown or HTML
- Supports different styling options
- Can generate summaries from crawled content

### Export Service

Converts rendered content to various file formats:
- PDF export
- DOCX (Microsoft Word) export
- Plain text export

## Getting Started

1. Set up the environment:
   ```bash
   pip install -r requirements.txt
   ```

2. Run a crawl job:
   ```bash
   python crawl_service/main.py
   ```
   Or with a config file:
   ```bash
   python crawl_service/main.py --config crawl_service/config/job.yaml
   ```

3. Render the crawled content:
   ```bash
   python render_service/main.py
   ```

4. Export to your desired format:
   ```bash
   python export_service/main.py --input render_service/output/rendered_output.md --format pdf
   ```

## Configuration

Each service can be configured through YAML files or interactive prompts:

- **Crawl Service**: Configure URLs, depth, and crawl modes
- **Render Service**: Choose rendering format and styling
- **Export Service**: Select output format and file location

## Workflow Example

1. Crawl a website and extract content:
   ```bash
   python crawl_service/main.py --config crawl_service/config/job.yaml
   ```

2. Render the crawled content to Markdown:
   ```bash
   python render_service/main.py --config render_service/config/render_job.yaml
   ```

3. Export the rendered content to PDF:
   ```bash
   python export_service/main.py --input render_service/output/rendered_output.md --format pdf --output export_service/output/final_document
   ```

## Dependencies

- crawl4ai: Web crawling engine
- pydantic: Data validation and settings management
- weasyprint: HTML to PDF conversion
- python-docx: DOCX file generation
