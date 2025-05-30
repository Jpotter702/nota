from pathlib import Path
from markdown2 import markdown
from weasyprint import HTML

def export(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_text = markdown(md_text)
    HTML(string=html_text).write_pdf(output_path)
    print(f"📄 PDF exported to {output_path}")