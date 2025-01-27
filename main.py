#!/usr/bin/env python
from typing import Optional
import sys
import subprocess
import os
import tempfile
from tqdm import tqdm
import time
import argparse
from lib.help_lib import help_string


def compile_markdown_to_pdf(
    source_file: str,
    output_pdf: Optional[str] = None,
    open_file: bool = False,
    save_file: bool = False
) -> None:
    """
    Compiles a Markdown file to a PDF using pdflatex, optionally saving or opening the file.
    Includes three nested helper functions, each returning something.

    1) convert_markdown_to_latex: Converts Markdown to LaTeX (side effect: writes .tex file).
    2) run_pdflatex: Runs pdflatex twice (side effect: writes .pdf file).
    3) open_pdf: Opens the PDF with the system's default viewer.

    :param source_file: The input Markdown file path.
    :param output_pdf: The output PDF file path (if saving).
    :param open_file: Whether to open the generated PDF in the system's default viewer.
    :param save_file: Whether to move the PDF out of the temp location into output_pdf.
    :return: None. Side effects are writing files and optionally opening the PDF.
    """

    def convert_markdown_to_latex(md_path: str, tex_path: str) -> str:
        subprocess.run(
            ['pandoc', md_path, '-s', '-o', tex_path, '--pdf-engine-opt=--quiet'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return tex_path

    def run_pdflatex(tex_file: str, output_dir: str) -> str:
        pdflatex_command = [
            'pdflatex',
            '-interaction=nonstopmode',
            '-output-directory', output_dir,
            tex_file
        ]
        # First pass
        subprocess.run(pdflatex_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Second pass
        subprocess.run(pdflatex_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        base_name = os.path.splitext(os.path.basename(tex_file))[0]
        return os.path.join(output_dir, f"{base_name}.pdf")

    def open_pdf(pdf_path: str) -> None:
        try:
            if sys.platform.startswith('darwin'):
                subprocess.run(['open', pdf_path], check=False)
            elif os.name == 'nt':
                os.startfile(pdf_path)  # type: ignore
            elif os.name == 'posix':
                subprocess.run(['xdg-open', pdf_path], check=False)
            #return f"Opened PDF: {pdf_path}"
            
        except Exception as e:
            print(f"Unable to open PDF automatically: {str(e)}")

    if not source_file.endswith('.md'):
        print("The source file must be a Markdown (.md) file.")
        sys.exit(1)

    total_steps = 3  # 1) pandoc, 2) pdflatex pass, 3) second pdflatex pass
    delay_per_step = 1

    with tempfile.NamedTemporaryFile(delete=False, suffix=".tex") as temp_tex_file:
        temp_tex_path: str = temp_tex_file.name

    final_pdf_path = ""

    try:
        # Set leave=False so that the progress bar does not remain or reprint at completion
        progress_bar = tqdm(
            total=total_steps,
            desc='Boom! Boom! Boom!',
            position=0,
            leave=False,
            bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
        )

        # Step 1
        convert_markdown_to_latex(source_file, temp_tex_path)
        time.sleep(delay_per_step)
        progress_bar.update(1)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Step 2 & 3
            generated_pdf: str = run_pdflatex(temp_tex_path, temp_dir)
            time.sleep(delay_per_step)
            progress_bar.update(1)

            time.sleep(delay_per_step)
            progress_bar.update(1)

            if not os.path.exists(generated_pdf):
                print("\nPDF was not generated as expected.")
                sys.exit(1)

            if output_pdf is None:
                # Default to source_file.pdf if no output path given
                output_pdf = os.path.splitext(source_file)[0] + ".pdf"

            if save_file:
                os.rename(generated_pdf, output_pdf)
                final_pdf_path = output_pdf
            else:
                final_pdf_path = generated_pdf

            if open_file:
                open_pdf(final_pdf_path)
                # print(status_message)

        # progress_bar.close()

        print(f"PDF generated at: {final_pdf_path}")

    except subprocess.CalledProcessError as e:
        print(f"\nError during compilation: {e}")
        sys.exit(1)
    finally:
        if os.path.exists(temp_tex_path):
            os.remove(temp_tex_path)

def setup_md2ltx_symlink():
    """
    Ensures the current script is executable (chmod +x) and sets up a symbolic link
    "/usr/local/bin/md2ltx" -> <this script's location>, unless it already exists.

    Requires root privileges or suitable permissions for /usr/local/bin.
    """
    # 1) Make sure our script is executable
    script_path = os.path.realpath(__file__)
    if not os.access(script_path, os.X_OK):
        try:
            print(f"Making the script executable: {script_path}")
            subprocess.run(["chmod", "+x", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to chmod +x on {script_path}\n{e}")
            return
    # else:
        # print(f"Script '{script_path}' is already executable. Skipping chmod +x.")

    # 2) Create or update the symlink in /usr/local/bin
    symlink_path = "/usr/local/bin/md2ltx"
    if os.path.islink(symlink_path) or os.path.exists(symlink_path):
        # Optional: Check if it already points to our script
        current_target = ""
        if os.path.islink(symlink_path):
            current_target = os.readlink(symlink_path)

        if current_target == script_path:
            # print(f"Symbolic link '{symlink_path}' already points to this script. Skipping creation.")
            return
        else:
            print(f"Removing existing file/link at '{symlink_path}' to update.")
            try:
                subprocess.run(["sudo", "rm", "-f", symlink_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove existing file or link at '{symlink_path}'.\n{e}")
                return

    # Now create the symlink
    try:
        print(f"Creating symbolic link: {symlink_path} -> {script_path}")
        subprocess.run(["sudo", "ln", "-s", script_path, symlink_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create symbolic link at {symlink_path}.\n{e}")


def main():

    setup_md2ltx_symlink()

    # We disable the default --help by setting add_help=False
    parser = argparse.ArgumentParser(
        description="Compile a Markdown (.md) file to PDF using Pandoc and pdflatex.",
        add_help=False
    )

    # Define a custom --help flag
    parser.add_argument(
        "--help",
        action="store_true",
        help="Show the help message and exit."
    )

    parser.add_argument(
        "source_file",
        nargs="?",
        help="Path to the input Markdown file."
    )

    parser.add_argument(
        "output_pdf",
        nargs="?",
        default=None,
        help="Path to the output PDF file (optional). If omitted, uses default naming."
    )

    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the resulting PDF with the system's default viewer."
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the resulting PDF to the specified output path (otherwise a temp file)."
    )

    # Parse arguments
    args = parser.parse_args()

    # If --help was passed, print our custom help string from help.py and exit.
    if args.help:
        print(help_string)
        sys.exit(0)

    # A minimal sanity check; if source_file isn't provided, show an error
    if not args.source_file:
        # print("Error: A source markdown file is required.")
        print("Use '--help' for more information.")
        sys.exit(1)

    # If the source file doesn't exist, let user know
    if not os.path.exists(args.source_file):
        print(f"Error: No such file '{args.source_file}'")
        sys.exit(1)

    compile_markdown_to_pdf(
        source_file=args.source_file,
        output_pdf=args.output_pdf,
        open_file=args.open,
        save_file=args.save
    )



if __name__ == "__main__":
    main()


