from typing import Optional
from pydantic import BaseModel

class CrawlJob(BaseModel):
    url: str
    max_depth: int = 2
    include_subdomains: bool = False
    obey_robots_txt: bool = True
    bypass_cache: bool = True
    output: Optional[str] = None        # 👈 Add this line
    json_extract: Optional[str] = None
    schema: Optional[str] = None
    filter_config: Optional[str] = None
