def export(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"📄 TXT exported to {output_path}")