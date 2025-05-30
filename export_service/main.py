"""
Export Service Main Module

This module provides functionality to export rendered markdown content to various file formats
including PDF, TXT, and DOCX. It serves as the final step in the Nota content processing pipeline.
"""

# Add the parent directory to the system path to allow importing from sibling directories
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from pathlib import Path

# Import the various exporters from the modules directory
from export_service.src.modules import pdf_exporter, txt_exporter, doc_exporter


def main():
    """
    Main function that orchestrates the export process:
    1. Parse command-line arguments
    2. Create output directory if needed
    3. Call the appropriate exporter based on the requested format
    4. Report completion status
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Export rendered markdown to desired format.")
    parser.add_argument("--input", required=True, help="Path to rendered markdown file")
    parser.add_argument("--format", choices=["pdf", "txt", "doc"], default="pdf", help="Export format")
    parser.add_argument("--output", default="export_service/output/final_output", help="Output file base name")
    args = parser.parse_args()

    # Ensure the output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Export to the requested format using the appropriate exporter
    if args.format == "pdf":
        pdf_exporter.export(args.input, f"{args.output}.pdf")
    elif args.format == "txt":
        txt_exporter.export(args.input, f"{args.output}.txt")
    elif args.format == "doc":
        doc_exporter.export(args.input, f"{args.output}.docx")
    else:
        # This should never happen due to the choices parameter in argparse,
        # but included as a safeguard
        raise ValueError(f"Unsupported format: {args.format}")

    # Report successful completion
    print(f"✅ Export completed: {args.output}.{args.format if args.format != 'doc' else 'docx'}")


if __name__ == "__main__":
    main()
