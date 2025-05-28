# crawl_service/src/main.py

import argparse
import asyncio
import json
import yaml
from pathlib import Path
from crawl4ai import AsyncWebCrawler
from shared.models.crawl_job import CrawlJob
from shared.utils.mode_router import apply_mode_to_job

def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_results(results, output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in results], f, indent=2)
    print(f"✅ Saved crawl results to {output_path}")

async def run_crawler(job: CrawlJob):
    crawler = AsyncWebCrawler()
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
    parser = argparse.ArgumentParser(description="Run a crawl job.")
    parser.add_argument("--config", type=str, required=True, help="Path to crawl job YAML config")
    args = parser.parse_args()

    raw_config = load_config(args.config)
    mode = raw_config.get("mode")
    if mode:
        print(f"⚙️  Applying mode: {mode}")
        config = apply_mode_to_job(mode, raw_config)
    else:
        config = raw_config

    job = CrawlJob(**config)
    results = asyncio.run(run_crawler(job))
    save_results(results, "crawl_service/output/results.json")

if __name__ == "__main__":
    main()
