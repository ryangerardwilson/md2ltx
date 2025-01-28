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
    template_name: Optional[str] = None,
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

    def convert_markdown_to_latex(md_path: str, tex_path: str, templates: dict, template_name: Optional[str] = None) -> str:
        # Build the base Pandoc command
        pandoc_cmd = [
            'pandoc', md_path,
            '-s',
            '-o', tex_path,
            '--pdf-engine-opt=--quiet'
        ]

        # print(templates)
        # <-- Added: If a template_name is given and it exists in templates, write to temp file and use it.
        if template_name and template_name in templates:
            # print(f"printing template {template_name}")
            # print(templates[template_name])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".tex") as tf:
                tf.write(templates[template_name].encode('utf-8'))
                tf.flush()
                pandoc_cmd.append(f'--template={tf.name}')

        subprocess.run(
            pandoc_cmd,
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
        subprocess.run(
            pdflatex_command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Second pass
        subprocess.run(
            pdflatex_command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

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

    templates = {

    "one-column-article": r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[lmargin=1in,rmargin=1in]{geometry}
\usepackage[unicode=true]{hyperref}
\usepackage{lmodern}
\providecommand{\tightlist}{
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}
}
\title{$title$}
\author{$author$}
\date{$date$}

\begin{document}
\maketitle
$body$
\end{document}
    """,

    "two-column-article": r"""
\documentclass[twocolumn]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[unicode=true]{hyperref}
\providecommand{\tightlist}{
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}
}
\title{$title$}
\author{$author$}
\date{$date$}

\begin{document}
\maketitle
$body$
\end{document}
""",

        "report": r"""
\documentclass{report}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=1in]{geometry}
\usepackage[unicode=true]{hyperref}
\providecommand{\tightlist}{
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}
}
\title{$title$}
\author{$author$}
\date{$date$}

\begin{document}
\maketitle
\tableofcontents
$body$
\end{document}
    """,

        "slides": r"""
\documentclass{beamer}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[unicode=true]{hyperref}
\title{$title$}
\subtitle{$subtitle$}
\author{$author$}
\date{$date$}

\begin{document}
\begin{frame}
\titlepage
\end{frame}
\begin{frame}{Outline}
\tableofcontents
\end{frame}
$body$
\end{document}
    """,

        "letter": r"""
\documentclass{letter}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=1in]{geometry}
\signature{$author$}
\address{$address$}
\date{$date$}

\begin{document}
\begin{letter}{$recipient$}
\opening{$greeting$}
$body$
\closing{$closing$}
\end{letter}
\end{document}
    """
    }

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




    try:
        progress_bar = tqdm(
            total=total_steps,
            desc='Boom! Boom! Boom!',
            position=0,
            leave=False,
            bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
        )

        convert_markdown_to_latex(source_file, temp_tex_path, templates, template_name)
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

def install_pandoc_and_latex():
    """
    Install pandoc and a set of essential TeX Live packages on an Ubuntu-like system
    (requires sudo privileges). This approach is more minimal than installing texlive-full,
    yet covers most common needs.
    
    # List of essential packages commonly used for LaTeX documents:
    #   texlive-latex-base           -> Basic LaTeX
    #   texlive-latex-recommended    -> Common document classes, packages (graphics, etc.)
    #   texlive-latex-extra          -> Extra packages often needed (like fancyhdr, wrapfig, etc.)
    #   texlive-fonts-recommended    -> Good set of fonts
    # You can add or remove packages if you find you need something more specialized.
    """
    packages = [
        "pandoc",
        "texlive-latex-base",
        "texlive-latex-recommended",
        "texlive-latex-extra",
        "texlive-fonts-recommended"
    ]

    print("Attempting to install pandoc and a minimal TeX Live set of packages...")
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "-y", "install"] + packages, check=True)
        print("Installation of pandoc and a minimal TeX Live environment completed.")
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

    # <-- Added: new argument for template name
    parser.add_argument(
        "--template",
        default=None,
        help="Name of a built-in template to use (e.g. 'two-column')."
    )

    args = parser.parse_args()

    # If --help was passed, show custom help and exit
    if args.help:
        print(help_string)
        sys.exit(0)

    # If --install was passed, attempt software install, then exit
    if args.install_dependencies:
        install_pandoc_and_latex()
        print("\nDependencies installed. Re-run md2ltx without --install_dependencies to compile documents.")
        sys.exit(0)

    # Minimal sanity check
    if not args.source_file:
        print("A source markdown file is required. Try --help for usage.")
        sys.exit(1)

    # Check that file exists
    if not os.path.exists(args.source_file):
        print(f"Error: No such file: {args.source_file}")
        sys.exit(1)

    # <-- Modified: pass template name along
    compile_markdown_to_pdf(
        source_file=args.source_file,
        output_pdf=args.output_pdf,
        template_name=args.template,
        open_file=args.open
    )


if __name__ == "__main__":
    main()
