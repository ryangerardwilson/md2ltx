import subprocess
import os
import sys
import tempfile


# flake8: noqa: E402
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/md2ltx/lib')))
from python_evaluation import evaluate_python_in_markdown_string


def test_evaluate_python_in_markdown_string():
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
        print("EVALUATED CONTENT")
        print("#################################################################")
        print(evaluated_content)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    test_evaluate_python_in_markdown_string()
