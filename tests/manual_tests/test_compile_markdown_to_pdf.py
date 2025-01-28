import subprocess
import os
import sys
import tempfile

# Insert parent directory (two levels up) to import main.py
# flake8: noqa: E402
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


from src.md2ltx.main import compile_markdown_to_pdf


def test_compile_markdown_to_pdf():
    markdown_content = r"""
---
title: "My Awesome Title"
author: "John Doe"
date: "October 4, 2023"
---

# Sample Document

This is a **Markdown** document to test `compile_markdown_to_pdf` from `main.py`.

## Advantages of Markdown

- Easy to write
- Human-readable
- Widely supported

## Conclusion

Markdown is fantastic!
    """

    # Create a temporary Markdown file
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_md_file:
        temp_md_path = temp_md_file.name
        temp_md_file.write(markdown_content.encode('utf-8'))

    # Define a temporary output PDF path
    output_pdf_path = tempfile.mktemp(suffix=".pdf")

    try:
        # Example usage:
        # compile_markdown_to_pdf(source_file, output_pdf, open_file, save_file)
        # 1) Save to output_pdf_path and also open it:
        compile_markdown_to_pdf(temp_md_path, output_pdf_path, template_name="two-column-article", open_file=True)

        # 2) If you wanted to just open without saving, you could do:
        # compile_markdown_to_pdf(temp_md_path, open_file=True, save_file=False)

        # 3) Or just save without opening:
        # compile_markdown_to_pdf(temp_md_path, output_pdf_path, open_file=False, save_file=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up the temporary Markdown file
        if os.path.exists(temp_md_path):
            os.remove(temp_md_path)

    print("Test completed!")


if __name__ == "__main__":
    test_compile_markdown_to_pdf()
