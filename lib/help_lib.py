help_string = r"""
===============================================================================
md2latex: A Command-Line Tool for Converting Markdown to PDF via Pandoc & LaTeX
===============================================================================

USAGE:
    md2ltx [source.md] [output.pdf] [--open] [--save] [--help]

POSITIONAL ARGUMENTS:
    source_file    Path to the input Markdown (.md) file.
    output_pdf     (Optional) Path to the output PDF file. If omitted, 
                   a default name is derived from the source file.

OPTIONAL SWITCHES:
    --open         Open the resulting PDF in the system's default viewer.
    --save         Save the resulting PDF to the provided output file instead 
                   of a temporary file.
    --help         Show this help message and exit.

DESCRIPTION:
    md2latex uses Pandoc to transform Markdown files into LaTeX, then invokes
    pdflatex to create a final PDF. This workflow supports most of Markdown’s 
    core syntax plus many Pandoc extensions.

    Below is a high-level, illustrative overview of how Pandoc typically converts
    various Markdown constructs into LaTeX. This list is not exhaustive, but it 
    captures many common syntax elements. Refer to the official Pandoc documentation 
    for the most detailed and up-to-date feature set.

-------------------------------------------------------------------------------
1) HEADINGS
-------------------------------------------------------------------------------
• Markdown:
      # Heading 1
      ## Heading 2
      ### Heading 3
      ...etc.

• Pandoc → LaTeX:
      \section{Heading 1}
      \subsection{Heading 2}
      \subsubsection{Heading 3}
      ...

Depending on the heading level, Pandoc chooses \section, \subsection, etc. It also
supports “underline” style headings like "===” and “---”.

-------------------------------------------------------------------------------
2) EMPHASIS & STRONG EMPHASIS
-------------------------------------------------------------------------------
• Markdown:
      *emphasis* or _emphasis_
      **strong emphasis** or __strong emphasis__

• Pandoc → LaTeX:
      \emph{emphasis}
      \textbf{strong emphasis}

-------------------------------------------------------------------------------
3) INLINE CODE
-------------------------------------------------------------------------------
• Markdown:
      `inline code`

• Pandoc → LaTeX:
      \texttt{inline code}

-------------------------------------------------------------------------------
4) CODE BLOCKS
-------------------------------------------------------------------------------
• Markdown (fenced code block):
      ```
      a = 1
      b = 2
      ```

• Pandoc → LaTeX (default):
      \begin{verbatim}
      a = 1
      b = 2
      \end{verbatim}

Pandoc can produce different environments (e.g., listings) with certain options.

-------------------------------------------------------------------------------
5) LISTS
-------------------------------------------------------------------------------
• Unordered lists:
      - item 1
      - item 2
      - item 3

  Pandoc → LaTeX:
      \begin{itemize}
      \item item 1
      \item item 2
      \item item 3
      \end{itemize}

• Ordered lists:
      1. item 1
      2. item 2

  Pandoc → LaTeX:
      \begin{enumerate}
      \item item 1
      \item item 2
      \end{enumerate}

-------------------------------------------------------------------------------
6) LINKS & IMAGES
-------------------------------------------------------------------------------
• Markdown (inline link):
      [Pandoc](https://pandoc.org)

  Pandoc → LaTeX:
      \href{https://pandoc.org}{Pandoc}

• Markdown (image):
      ![Alt text](image.png)

  Pandoc → LaTeX:
      \includegraphics{image.png}

By default, \includegraphics is placed without additional floats. Options exist 
for figure environments, captions, etc.

-------------------------------------------------------------------------------
7) BLOCKQUOTES
-------------------------------------------------------------------------------
• Markdown:
      > This is a blockquote.

  Pandoc → LaTeX:
      \begin{quote}
      This is a blockquote.
      \end{quote}

-------------------------------------------------------------------------------
8) HORIZONTAL RULES
-------------------------------------------------------------------------------
• Markdown:
      ---
      ***
      ___

  Pandoc → LaTeX:
      \hrule

-------------------------------------------------------------------------------
9) FOOTNOTES (Pandoc Extension)
-------------------------------------------------------------------------------
• Markdown:
      A footnote here.[^1]

      [^1]: Footnote text.

  Pandoc → LaTeX:
      A footnote here.\footnote{Footnote text.}

-------------------------------------------------------------------------------
10) TABLES
-------------------------------------------------------------------------------
• Markdown (simple pipe table):
      | Column1 | Column2 |
      |---------|---------|
      | Val1    | Val2    |

  Pandoc → LaTeX:
      \begin{table}
      \centering
      \begin{tabular}{ll}
      \hline
      Column1 & Column2 \\
      \hline
      Val1 & Val2 \\
      \hline
      \end{tabular}
      \end{table}

-------------------------------------------------------------------------------
11) MATH & LaTeX BLOCKS
-------------------------------------------------------------------------------
• Inline math:
      $E = mc^2$

  Pandoc → LaTeX:
      \( E = mc^2 \)

• Display math:
      $$
      E = mc^2
      $$

  Pandoc → LaTeX:
      \[
      E = mc^2
      \]

-------------------------------------------------------------------------------
12) CITATIONS & BIBLIOGRAPHIES
-------------------------------------------------------------------------------
Pandoc supports citations with a bibliography file. For instance,
      [@smith2009]
can become \cite{smith2009} in LaTeX via Pandoc’s citeproc or bibliography features.

-------------------------------------------------------------------------------
13) METADATA & TITLE BLOCKS
-------------------------------------------------------------------------------
YAML metadata (like “title: My Title”) can become \title{...}, \author{...}, etc.
Use “-s” or “--standalone” to generate a title page in LaTeX with \maketitle.

-------------------------------------------------------------------------------
14) RAW LaTeX
-------------------------------------------------------------------------------
Pandoc passes raw LaTeX through if the output is LaTeX or PDF. For example:
      \newpage
remains \newpage in the output.

-------------------------------------------------------------------------------
CONCLUSION: EXTENSIVE PANDOC CAPABILITIES
-------------------------------------------------------------------------------
Pandoc is a powerful, configurable tool for converting among multiple document 
formats. It parses your Markdown into an AST, then renders that AST to LaTeX 
(or any other target format) according to Pandoc’s rules and templates.

For more details:
• Pandoc User’s Guide: https://pandoc.org/MANUAL.html
• Pandoc Demos:       https://pandoc.org/demos.html

This makes Pandoc one of the most robust ways to convert Markdown to LaTeX 
(and many other output formats). Enjoy using md2latex!
"""
