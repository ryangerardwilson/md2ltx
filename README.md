# md2ltx

A command-line tool for converting Markdown to PDF via Pandoc and LaTeX. Requires a pip virtual environment in Ubuntu/ Debian based OS.

## 1. Quickstart

### 1.1. Installation

    pip install md2ltx; md2ltx --install_dependencies

### 1.2. Usage

    md2ltx [source.md] [output.pdf] [--open] [--help]

• `source_file`: Path to the input Markdown (.md) file.  

• `output_pdf` (optional): Path to the output PDF file. If omitted, a default name is derived from the source file, and the working directory is assumed to be the path.  

• `--open`: Open the resulting PDF in the system’s default viewer.  

• `--template &lt;template_name&gt;`: Specify a built-in templates by name. Available templates: “two-column”).

• `--help`: Access documentation.

## 2. Templates

md2ltx supports injecting Markdown content into a LaTeX “template” that defines the overall look and structure of the PDF. 

You can choose one of the built-in templates: "two-column". Using the “--template” flag tells Pandoc to load and apply that LaTeX template. Inside the template, Pandoc replaces special variables like `$title$`, `$author$`, `$date$`, and `$body$` with metadata and the converted Markdown content.

Pandoc reads title, author, and date from the YAML metadata block at the top of your Markdown file. For example:

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


Pandoc will inject your Markdown content where  `$body$` is defined, and the YAML metadata (title, author, date) will appear in your final PDF, as below.

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

---

## 3. General Pandoc Tranformations

md2ltx uses Pandoc to transform Markdown files into LaTeX, which pdflatex then uses to generate a final PDF. This workflow supports most of Markdown’s core syntax plus many Pandoc extensions. Below is a high-level overview of how Pandoc typically converts various Markdown constructs into LaTeX. For full details, refer to Pandoc’s official documentation.

---

### 3.1. Headings

• <strong>Markdown</strong>  
  <pre><code># Heading 1  
## Heading 2  
### Heading 3</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\section{Heading 1}  
\subsection{Heading 2}  
\subsubsection{Heading 3}</code></pre>

Pandoc chooses <code>\section</code>, <code>\subsection</code>, etc. based on the heading level. It also supports underline-style Markdown headings with “===” or “---” for level-one and level-two headings.

---

### 3.2. Emphasis &amp; Strong Emphasis

• <strong>Markdown</strong>  
  <pre><code>*emphasis* or _emphasis_  
**strong emphasis** or __strong emphasis__</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\emph{emphasis}  
\textbf{strong emphasis}</code></pre>

---

### 3.3. Inline Code

• <strong>Markdown</strong>  
  <pre><code>`inline code`</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\texttt{inline code}</code></pre>

---

### 3.4. Code Blocks

• <strong>Markdown (fenced)</strong>  
  <pre><code>```  
a = 1  
b = 2  
```</code></pre>

• <strong>Pandoc → LaTeX (by default)</strong>  
  <pre><code>\begin{verbatim}  
a = 1  
b = 2  
\end{verbatim}</code></pre>

With certain options, Pandoc can use different LaTeX environments (e.g., listings).

---

### 3.5. Lists

• <strong>Unordered (Markdown)</strong>  
  <pre><code>- item 1  
- item 2  
- item 3</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\begin{itemize}  
\item item 1  
\item item 2  
\item item 3  
\end{itemize}</code></pre>

• <strong>Ordered (Markdown)</strong>  
  <pre><code>1. item 1  
2. item 2</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\begin{enumerate}  
\item item 1  
\item item 2  
\end{enumerate}</code></pre>

---

### 3.6. Links &amp; Images

• <strong>Link (Markdown)</strong>  
  <pre><code>[Pandoc](https://pandoc.org)</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\href{https://pandoc.org}{Pandoc}</code></pre>

• <strong>Image (Markdown)</strong>  
  <pre><code>![Alt text](image.png)</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\includegraphics{image.png}</code></pre>

By default, <code>\includegraphics</code> is placed without floats. You can add captions or figure environments using extended syntax or metadata.

---

### 3.7. Blockquotes

• <strong>Markdown</strong>  
  <pre><code>> This is a blockquote.</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\begin{quote}  
This is a blockquote.  
\end{quote}</code></pre>

---

### 3.8. Horizontal Rules

• <strong>Markdown</strong>  
  <pre><code>---  
***  
___</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\hrule</code></pre>

---

### 3.9. Footnotes (Pandoc Extension)

• <strong>Markdown</strong>  
  <pre><code>This is some text with a footnote.[^1]

[^1]: This is the footnote text.</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>This is some text with a footnote.\footnote{This is the footnote text.}</code></pre>

---

### 3.10. Tables

• <strong>Markdown (simple pipe table)</strong>  
  <pre><code>| Column1 | Column2 |  
|---------|---------|  
| Val1    | Val2    |  
| Val3    | Val4    |</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\begin{table}  
\centering  
\begin{tabular}{ll}  
\hline  
Column1 & Column2 \\  
\hline  
Val1    & Val2    \\  
Val3    & Val4    \\  
\hline  
\end{tabular}  
\end{table}</code></pre>

---

### 3.11. Math &amp; LaTeX Blocks

• <strong>Inline Math</strong>  
  <pre><code>$E = mc^2$</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\(E = mc^2\)</code></pre>

• <strong>Display Math</strong>  
  <pre><code>$$  
E = mc^2  
$$</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\[  
E = mc^2  
\]</code></pre>

---

### 3.12. Citations &amp; Bibliographies

Pandoc can handle citations if you provide a bibliography file. A reference like <code>[@smith2009]</code> can become <code>\cite{smith2009}</code> or <code>\autocite</code> depending on the style and Pandoc’s command-line options.

---

### 3.14. Raw LaTeX

Pandoc passes raw LaTeX through if you’re converting to LaTeX or PDF. For example:

```
\newpage
```

remains <code>\newpage</code> in the output.

---


