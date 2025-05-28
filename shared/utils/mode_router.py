# shared/utils/mode_router.py

def apply_mode_to_job(mode: str, job: dict) -> dict:
    """
    Apply mode-based defaults to a job config dictionary.
    """
    updated = job.copy()

    if mode == "json":
        updated["output"] = "json"

    elif mode == "markdown":
        updated["output"] = "markdown"

    elif mode == "markdown-fit":
        updated["output"] = "markdown-fit"
        updated.setdefault("filter_config", "crawl_service/config/clean_content.yaml")

    elif mode == "html":
        updated["output"] = "html"

    elif mode == "html-fit":
        updated["output"] = "html-fit"
        updated.setdefault("filter_config", "crawl_service/config/clean_content.yaml")

    elif mode == "json_extract":
        updated["output"] = "markdown-fit"
        updated["json_extract"] = (
            job.get("json_extract")
            or "Summarize this page in 3-5 sentences."
        )
        updated.setdefault("filter_config", "crawl_service/config/clean_content.yaml")

    elif mode == "schema":
        updated["output"] = "json"
        updated.setdefault("schema", "crawl_service/config/schema.json")
        updated.setdefault("filter_config", "crawl_service/config/clean_content.yaml")

    elif mode == "filter_only":
        updated.setdefault("output", "markdown-fit")
        updated.setdefault("filter_config", "crawl_service/config/clean_content.yaml")

    else:
        raise ValueError(f"Unsupported mode: {mode}")

    return updated