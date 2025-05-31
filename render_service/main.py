"""
Render Service Main Module

This module processes crawled data into readable formats like markdown or HTML.
It serves as the middle step in the Nota content processing pipeline, taking
crawled data from the Crawl Service and preparing it for the Export Service.
"""

# Add the parent directory to the system path to allow importing from sibling directories
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import json
from pathlib import Path
import yaml

def prompt_for_config() -> dict:
    """
    Interactive command-line interface to collect rendering configuration from the user.
    
    Returns:
        dict: A dictionary containing the rendering configuration
    """
    # Get the path to the crawl results file
    input_path = input("Path to crawl results JSON: ") or "crawl_service/output/results.json"
    
    # Display and collect the render mode
    print("\nChoose render mode:")
    print("1. fit_markdown")
    print("2. html")
    print("3. markdown")
    print("4. summary (json_extract)")
    print("5. fit_html")
    
    # Map numeric choices to mode names
    mode_map = {
        "1": "fit_markdown",
        "2": "html",
        "3": "markdown",
        "4": "summary",
        "5": "fit_html"
    }
    choice = input("Your choice [1-5]: ") or "1"
    mode = mode_map.get(choice, "fit_markdown")

    # Get the output file path
    output_path = input("Output path (default: render_service/output/rendered_output.md): ") or "render_service/output/rendered_output.md"
    
    # Return the complete configuration
    return {
        "input_path": input_path,
        "mode": mode,
        "output_path": output_path
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

def load_crawl_results(input_path: str):
    """
    Load crawl results from a JSON file.
    
    Args:
        input_path (str): Path to the crawl results JSON file
        
    Returns:
        list: The loaded crawl results
    """
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_to_markdown(results: list, field: str = "fit_markdown") -> str:
    """
    Render crawl results to markdown format.
    
    Args:
        results (list): List of crawl result objects
        field (str): Field to use for content (default: "fit_markdown")
        
    Returns:
        str: The rendered markdown content
    """
    output = []
    skipped = 0
    for page in results:
        title = page.get("title", "Untitled")
        url = page.get("url", "")
        content = page.get(field)

        if content:
            output.append(f"# {title}\n\n[Source]({url})\n\n{content}\n\n---\n")
        else:
            skipped += 1
    print(f"✅ Rendered {len(output)} pages | Skipped {skipped} (no '{field}')")
    return "\n".join(output)

def save_output(content: str, output_path: str):
    """
    Save rendered content to a file.
    
    Args:
        content (str): The content to save
        output_path (str): Path where the content should be saved
    """
    # Create parent directories if they don't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Write content to the file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Rendered output saved to {output_path}")

def main():
    """
    Main function that orchestrates the rendering process:
    1. Parse command-line arguments
    2. Load or prompt for configuration
    3. Load crawl results
    4. Render the content
    5. Save the rendered output
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Render crawl results to markdown.")
    parser.add_argument("--config", type=str, help="Path to render profile YAML")
    args = parser.parse_args()

    # Load configuration from file or prompt the user
    if args.config:
        config = load_config(args.config)
    else:
        config = prompt_for_config()

    # Load the crawl results
    results = load_crawl_results(config["input_path"])

    # Detect which field to render based on chosen mode
    mode_to_field = {
        "markdown": "markdown",
        "fit_markdown": "fit_markdown",
        "html": "html",
        "fit_html": "fit_html",
        "summary": "summary"
    }
    field = mode_to_field.get(config["mode"], "fit_markdown")

    # Render the content to markdown
    content = render_to_markdown(results, field=field)
    
    # Save the rendered output
    save_output(content, config.get("output_path", "render_service/output/rendered_output.md"))

if __name__ == "__main__":
    main()
