import sys
import subprocess
import os
import tempfile
from tqdm import tqdm
import time
import argparse
import shutil
from typing import Optional

from md2ltx.lib.string_lib import logo_string, help_string

def compile_markdown_to_pdf(
    source_file: str,
    output_pdf: Optional[str] = None,
    open_file: bool = False
) -> None:
    """
    Compiles a Markdown file to a PDF using pdflatex, optionally saving or opening the file.

    1) convert_markdown_to_latex: Converts Markdown to LaTeX (side effect: writes .tex file).
    2) run_pdflatex: Runs pdflatex twice (side effect: writes .pdf file).
    3) open_pdf: Opens the PDF with the system's default viewer.

    Behavior:
    - If output_pdf is provided, the PDF will be placed there (and kept).
    - If no output_pdf is provided, it is written to the current working directory
      as <source_file_basename>.pdf, opened if requested, and then removed afterward.

    :param source_file: The input Markdown file path.
    :param output_pdf: The output PDF file path (optional).
    :param open_file: Whether to open the generated PDF in the system's default viewer.
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
        except Exception as e:
            print(f"Unable to open PDF automatically: {str(e)}")

    # Basic check – must be a .md file
    if not source_file.endswith('.md'):
        print("Error: The source file must be a Markdown (.md) file.")
        sys.exit(1)

    total_steps = 3  # 1) pandoc, 2) pdflatex pass, 3) second pdflatex pass
    delay_per_step = 1

    # Step 1: Convert Markdown to a temporary .tex file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tex") as temp_tex_file:
        temp_tex_path: str = temp_tex_file.name

    temp_dir = None
    final_pdf_path = None
    remove_after_open = False  # Will become True if no output_pdf is provided

    try:
        progress_bar = tqdm(
            total=total_steps,
            desc='Boom! Boom! Boom!',
            position=0,
            leave=False,
            bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
        )

        convert_markdown_to_latex(source_file, temp_tex_path)
        time.sleep(delay_per_step)
        progress_bar.update(1)

        # Create a temporary directory for pdflatex output
        temp_dir = tempfile.mkdtemp()

        # Run pdflatex
        generated_pdf = run_pdflatex(temp_tex_path, temp_dir)
        time.sleep(delay_per_step)
        progress_bar.update(1)

        time.sleep(delay_per_step)
        progress_bar.update(1)

        if not os.path.exists(generated_pdf):
            print("\nPDF was not generated as expected.")
            sys.exit(1)

        # If no output path is given, store in current working dir (pwd) & remove after opening
        if output_pdf is None:
            pdf_basename = os.path.splitext(os.path.basename(source_file))[0] + ".pdf"
            final_pdf_path = os.path.join(os.getcwd(), pdf_basename)
            # remove_after_open = True
        else:
            final_pdf_path = output_pdf

        # Move PDF to final path
        if os.path.exists(final_pdf_path):
            os.remove(final_pdf_path)
        os.rename(generated_pdf, final_pdf_path)

        # Open if requested
        if open_file:
            open_pdf(final_pdf_path)

        print(f"PDF generated at: {final_pdf_path}")

    except subprocess.CalledProcessError as e:
        print(f"\nError during compilation: {e}")
        sys.exit(1)

    finally:
        if os.path.exists(temp_tex_path):
            os.remove(temp_tex_path)

        if temp_dir and os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)

        # If we used a local PDF with no user-specified output, remove it afterward
        # if remove_after_open and final_pdf_path and os.path.exists(final_pdf_path):
        #    os.remove(final_pdf_path)


def install_pandoc_and_latex():
    """
    Install pandoc and a minimal TeX Live package on an Ubuntu-like system
    (requires sudo privileges). Adjust or extend for other operating systems.
    """
    print("Attempting to install pandoc and a minimal TeX Live distribution...")
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "-y", "install", "pandoc", "texlive-latex-base"], check=True)
        print("Installation of pandoc and TeX Live completed.")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")


def main():
    print(logo_string)

    parser = argparse.ArgumentParser(
        description="Compile a Markdown (.md) file to PDF using pandoc and pdflatex.",
        add_help=False
    )

    parser.add_argument(
        "--help",
        action="store_true",
        help="Show the help message and exit."
    )
    parser.add_argument(
        "--install_dependencies",
        action="store_true",
        help="Install pandoc and TeX Live (Ubuntu/Debian)."
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
        help="Path to the output PDF file (optional). If omitted, a temp PDF is created in the current directory and removed afterward."
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the resulting PDF with the system's default viewer."
    )

    args = parser.parse_args()

    # If --help was passed, show custom help and exit
    if args.help:
        print(help_string)
        sys.exit(0)

    # If --install was passed, attempt software install, then exit
    if args.install_dependencies:
        install_pandoc_and_latex()
        print("\nDependencies installed. Re-run md2ltx without --install to compile documents.")
        sys.exit(0)

    # Minimal sanity check
    if not args.source_file:
        print("Error: A source markdown file is required. Try --help for usage.")
        sys.exit(1)

    # Check that file exists
    if not os.path.exists(args.source_file):
        print(f"Error: No such file: {args.source_file}")
        sys.exit(1)

    # Compile
    compile_markdown_to_pdf(
        source_file=args.source_file,
        output_pdf=args.output_pdf,
        open_file=args.open
    )


if __name__ == "__main__":
    main()

