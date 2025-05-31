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
import importlib


def get_exporter(format_type: str):
    """
    Dynamically import and return the appropriate exporter module based on the requested format.
    
    Args:
        format_type (str): The export format type ('pdf', 'txt', or 'doc')
        
    Returns:
        module: The imported exporter module
    """
    if format_type == "pdf":
        return importlib.import_module("export_service.src.modules.pdf_exporter")
    elif format_type == "txt":
        return importlib.import_module("export_service.src.modules.txt_exporter")
    elif format_type == "doc":
        return importlib.import_module("export_service.src.modules.doc_exporter")
    else:
        raise ValueError(f"Unsupported format: {format_type}")


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

    # Only import the specific exporter module needed
    try:
        exporter = get_exporter(args.format)
        
        # Create the output filename with the appropriate extension
        output_filename = f"{args.output}.{args.format if args.format != 'doc' else 'docx'}"
        
        # Call the export function from the dynamically loaded module
        exporter.export(args.input, output_filename)
        
        # Report successful completion
        print(f"✅ Export completed: {output_filename}")
    except Exception as e:
        print(f"❌ Export failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
