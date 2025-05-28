from pydantic import BaseModel
from typing import Literal, Optional

class RenderJob(BaseModel):
    input_path: str                      # Path to crawl result JSON
    output_path: str                     # Path to save rendered output
    format: Literal['html', 'markdown', 'pdf'] = 'markdown'  # Output format
    title: Optional[str] = None          # Optional document title
    style: Optional[str] = 'classic'     # Optional render style (classic, modern, etc.)
