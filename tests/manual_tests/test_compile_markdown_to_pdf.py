import subprocess
import os
import sys
import tempfile

# flake8: noqa: E402
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.md2ltx.main import compile_markdown_to_pdf

# flake8: noqa: E402
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/md2ltx/lib')))
from constants import templates
from python_evaluation import evaluate_python_in_markdown_string


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

Markdown is fantastic! `EMBED::sqrt_of_16`. Markdown is fantastic2! `EMBED::compute_2`.

And this is incomingcalls: `EMBED::eval_3`

[START]#########################################################################
    def sqrt_of_16() -> str:
        val = math.sqrt(16)
        print("huhuhahah")
        return f"The square root of 16 is {val}"
[END]###########################################################################

[START]#########################################################################
    def compute_2() -> str:
        val = math.sqrt(25)
        return f"The square root of 25 is {val}"

    def eval_3() -> str:
        df = rgwfuncs.load_data_from_query("happy","SELECT * FROM incomingcalls LIMIT 20")
        df_first_three_cols = df.iloc[:, :3]
        return df_first_three_cols

[END]###########################################################################
    """

    try:
        evaluated_content = evaluate_python_in_markdown_string(markdown_content)

        # Create a temporary Markdown file
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_md_file:
            temp_md_path = temp_md_file.name
            temp_md_file.write(evaluated_content.encode('utf-8'))

        # Define a temporary output PDF path
        output_pdf_path = tempfile.mktemp(suffix=".pdf")

        # get the base name of the file (e.g., file.md)
        base_name = os.path.basename(temp_md_path)
        # split the base name to remove the extension (e.g., ['file', 'md'])
        source_file_name_without_extension = os.path.splitext(base_name)[0]

        compile_markdown_to_pdf(
            source_file_name_without_extension=source_file_name_without_extension,
            preprocessed_source_file=temp_md_path,
            output_pdf=output_pdf_path,
            template_content=templates.get("two-column-article"),
            open_file=True,
        )
    except Exception as e:
        print(e)

    finally:
        if os.path.exists(temp_md_path):
            os.remove(temp_md_path)

    print("Test completed!")


if __name__ == "__main__":
    test_compile_markdown_to_pdf()
