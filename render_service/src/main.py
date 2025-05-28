# render_service/src/main.py

import argparse
import json
from pathlib import Path
import yaml

def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_crawl_results(input_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_to_markdown(results: list, use_summary: bool = False) -> str:
    output = []
    for page in results:
        title = page.get("title", "Untitled")
        url = page.get("url", "")
        content = page.get("summary") if use_summary else page.get("fit_markdown")

        output.append(f"# {title}\n\n[Source]({url})\n\n{content}\n\n---\n")
    return "\n".join(output)

def save_output(content: str, output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Rendered output saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Render crawl results to markdown.")
    parser.add_argument("--config", type=str, required=True, help="Path to render profile YAML")
    args = parser.parse_args()

    config = load_config(args.config)
    results = load_crawl_results(config["input_path"])
    mode = config.get("mode", "markdown-fit")
    use_summary = mode == "json_extract"

    content = render_to_markdown(results, use_summary=use_summary)
    save_output(content, config.get("output_path", "render_service/output/rendered_output.md"))

if __name__ == "__main__":
    main()
