# export_service/main.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import argparse
from pathlib import Path

from export_service.src.modules import pdf_exporter, txt_exporter, doc_exporter


def main():
    parser = argparse.ArgumentParser(description="Export rendered markdown to desired format.")
    parser.add_argument("--input", required=True, help="Path to rendered markdown file")
    parser.add_argument("--format", choices=["pdf", "txt", "doc"], default="pdf", help="Export format")
    parser.add_argument("--output", default="export_service/output/final_output", help="Output file base name")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "pdf":
        pdf_exporter.export(args.input, f"{args.output}.pdf")
    elif args.format == "txt":
        txt_exporter.export(args.input, f"{args.output}.txt")
    elif args.format == "doc":
        doc_exporter.export(args.input, f"{args.output}.docx")
    else:
        raise ValueError(f"Unsupported format: {args.format}")

    print(f"✅ Export completed: {args.output}.{args.format if args.format != 'doc' else 'docx'}")


if __name__ == "__main__":
    main()
