# render_service/main.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import argparse
import json
from pathlib import Path
import yaml

def prompt_for_config() -> dict:
    input_path = input("Path to crawl results JSON: ") or "crawl_service/output/results.json"
    
    print("\nChoose render mode:")
    print("1. fit_markdown")
    print("2. html")
    print("3. markdown")
    print("4. summary (json_extract)")
    print("5. fit_html")
    
    mode_map = {
        "1": "fit_markdown",
        "2": "html",
        "3": "markdown",
        "4": "summary",
        "5": "fit_html"
    }
    choice = input("Your choice [1-5]: ") or "1"
    mode = mode_map.get(choice, "fit_markdown")

    output_path = input("Output path (default: render_service/output/rendered_output.md): ") or "render_service/output/rendered_output.md"
    return {
        "input_path": input_path,
        "mode": mode,
        "output_path": output_path
    }

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
    parser.add_argument("--config", type=str, help="Path to render profile YAML")
    args = parser.parse_args()

    if args.config:
        config = load_config(args.config)
    else:
        config = prompt_for_config()

    results = load_crawl_results(config["input_path"])
    use_summary = config.get("mode") == "json_extract"
    content = render_to_markdown(results, use_summary=use_summary)
    save_output(content, config.get("output_path", "render_service/output/rendered_output.md"))

if __name__ == "__main__":
    main()
