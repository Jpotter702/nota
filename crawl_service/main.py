"""
Crawl Service Main Module

This module provides the main functionality for the web crawling service.
It handles configuration loading, running the crawler, and saving results.
"""

import sys
from pathlib import Path
# Add the parent directory to the system path to allow importing from sibling directories
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import asyncio
import json
import yaml

from crawl4ai import AsyncWebCrawler
from shared.models.crawl_job import CrawlJob
from shared.utils.mode_router import apply_mode_to_job

def prompt_for_config() -> dict:
    """
    Interactive command-line interface to collect crawl configuration from the user.
    
    Returns:
        dict: A dictionary containing the crawl configuration
    """
    # Collect basic crawl parameters
    url = input("Enter the website URL to crawl: ") or "https://example.com"
    max_depth = int(input("Enter crawl depth (default 1): ") or 1)
    include_subdomains = input("Include subdomains? (y/n): ").lower().startswith("y")
    obey_robots_txt = input("Obey robots.txt? (y/n): ").lower().startswith("y")
    
    # Display and collect the crawl mode
    print("\nChoose crawl mode:")
    print("1. markdown")
    print("2. markdown-fit")
    print("3. html")
    print("4. html-fit")
    print("5. summary (json_extract)")
    print("6. schema")
    print("7. filter_config")

    # Map numeric choices to mode names
    mode_map = {
        "1": "markdown",
        "2": "markdown-fit",
        "3": "html",
        "4": "html-fit",
        "5": "summary",
        "6": "schema",
        "7": "filter_config"
    }
    choice = input("Your choice [1-7]: ") or "2"
    mode = mode_map.get(choice, "markdown-fit")

    # Return the complete configuration
    return {
        "url": url,
        "max_depth": max_depth,
        "include_subdomains": include_subdomains,
        "obey_robots_txt": obey_robots_txt,
        "bypass_cache": True,
        "mode": mode
    }

def load_config(path: str) -> dict:
    """
    Load configuration from a YAML file.
    
    Args:
        path (str): Path to the YAML configuration file
        
    Returns:
        dict: The loaded configuration
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_results(results, output_path: str):
    """
    Save the crawl results to a JSON file.
    
    Args:
        results: The crawl results to save
        output_path (str): Path where the results should be saved
    """
    # Create parent directories if they don't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Write results to the JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in results], f, indent=2)
    print(f"✅ Saved crawl results to {output_path}")

async def run_crawler(job: CrawlJob):
    """
    Run the web crawler with the provided job configuration.
    
    Args:
        job (CrawlJob): The crawl job configuration
        
    Returns:
        The results from the crawler
    """
    # Initialize the crawler
    crawler = AsyncWebCrawler()
    
    # Run the crawler with the job parameters
    results = await crawler.arun(
        url=job.url,
        max_depth=job.max_depth,
        include_subdomains=job.include_subdomains,
        obey_robots_txt=job.obey_robots_txt,
        bypass_cache=job.bypass_cache,
        output=job.output,
        json_extract=job.json_extract,
        schema=job.schema,
        filter_config=job.filter_config,
    )
    return results

def main():
    """
    Main function that orchestrates the crawl process:
    1. Parse command-line arguments
    2. Load or prompt for configuration
    3. Apply mode-specific settings
    4. Run the crawler
    5. Save the results
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Run a crawl job.")
    parser.add_argument("--config", type=str, help="Path to crawl job YAML config")
    args = parser.parse_args()

    # Load configuration from file or prompt the user
    if args.config:
        raw_config = load_config(args.config)
    else:
        raw_config = prompt_for_config()

    # Apply mode-specific settings if a mode is specified
    mode = raw_config.get("mode")
    if mode:
        print(f"⚙️  Applying mode: {mode}")
        config = apply_mode_to_job(mode, raw_config)
    else:
        config = raw_config

    # Create the CrawlJob object and run the crawler
    job = CrawlJob(**config)
    results = asyncio.run(run_crawler(job))
    
    # Save the results to a JSON file
    save_results(results, "crawl_service/output/results.json")

if __name__ == "__main__":
    main()
