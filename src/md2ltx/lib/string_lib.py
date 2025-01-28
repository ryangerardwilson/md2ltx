logo_string = r"""

                                         _______              .-''-.     .---.
                         __  __   ___    \  ___ `'.         .' .-.  )    |   |
                        |  |/  `.'   `.   ' |--.\  \       / .'  / /     |   |
                        |   .-.  .-.   '  | |    \  '     (_/   / /      |   |      .|
                        |  |  |  |  |  |  | |     |  '         / /       |   |    .' |_     ____     _____
                        |  |  |  |  |  |  | |     |  |        / /        |   |  .'     |   `.   \  .'    /
                        |  |  |  |  |  |  | |     ' .'       . '         |   | '--.  .-'     `.  `'    .'
                        |  |  |  |  |  |  | |___.' /'       / /    _.-') |   |    |  |         '.    .'
                        |__|  |__|  |__| /_______.'/      .' '  _.'.-''  |   |    |  |         .'     `.
                                         \_______|/      /  /.-'_.'      '---'    |  '.'     .'  .'`.   `.
                                                        /    _.'                  |   /    .'   /    `.   `.
                                                       ( _.-'                     `'-'    '----'       '----'

                     (
        (            )\ )                           (                                   (        (  (           (
        )\          (()/(   (         )             )\ )       (    (        )   (      )\ )     )\))(   ' (    )\
  __  (((_)  __      /(_))  )\ )   ( /(    (       (()/(      ))\   )(    ( /(   )(    (()/(    ((_)()\ )  )\  ((_)  (     (     (
 / /  )\___  \ \    (_))   (()/(   )(_))   )\ )     /(_))_   /((_) (()\   )(_)) (()\    ((_))   _(())\_)()((_)  _    )\    )\    )\ )
| |  ((/ __|  | |   | _ \   )(_)) ((_)_   _(_/(    (_)) __| (_))    ((_) ((_)_   ((_)   _| |    \ \((_)/ / (_) | |  ((_)  ((_)  _(_/(
| |   | (__   | |   |   /  | || | / _` | | ' \))     | (_ | / -_)  | '_| / _` | | '_| / _` |     \ \/\/ /  | | | |  (_-< / _ \ | ' \))
 \_\   \___| /_/    |_|_\   \_, | \__,_| |_||_|       \___| \___|  |_|   \__,_| |_|   \__,_|      \_/\_/   |_| |_|  /__/ \___/ |_||_|
                            |__/
######################################################################################################################################

"""


help_string = r"""
# md2ltx

A command-line tool for converting Markdown to LateX-formatted PDF via Pandoc. Requires a pip virtual environment in Ubuntu/ Debian based OS.

## 1. Quickstart

### 1.1. Installation

    pip install md2ltx; md2ltx --install_dependencies

### 1.2. Usage

    md2ltx [source.md] [output.pdf] [--open] [--help]

• `source_file`: Path to the input Markdown (.md) file.  

• `output_pdf` (optional): Path to the output PDF file. If omitted, a default name is derived from the source file, and the working directory is assumed to be the path.  

• `--open`: Open the resulting PDF in the system’s default viewer.  

• `--template template_name`: Specify a built-in templates by name. Available templates: "one-column-article", "two-column-article", "report", "slides", "letter").

• `--help`: Access documentation.

--------------------------------------------------------------------------------

## 2. Templates

md2ltx can inject Markdown content into a LaTeX “template” that defines the overall look and structure of the PDF. You can choose from these built-in templates:

• "one-column-article"  
• "two-column-article"  
• "report"  
• "slides"  
• "letter"

When you run md2ltx (or Pandoc directly), you can specify the template with the “--template” flag. Pandoc then loads that template, replacing special variables like $title$, $author$, $date$, and $body$ with metadata and the converted Markdown content.

### 2.1. Common Fields in the YAML Metadata

• one-column-article/ two-column-article / report:  
  - title: Title of your document  
  - author: Author name(s)  
  - date: Date displayed below the author(s)

• slides (Beamer presentations):  
  - title: Presentation title  
  - subtitle: (Optional) subtitle for your presentation  
  - author: Presenter name(s)  
  - date: Date (often included on the title slide)

• letter:  
  - author: Sender’s name (also used in \signature)  
  - address: Sender’s address  
  - date: Date displayed in the letter  
  - recipient: Recipient name or address  
  - greeting: Opening phrase (e.g., “Dear John,”)  
  - closing: Closing phrase (e.g., “Regards,”)

-------------------------------------------------------------------------------
### 2.2. Using the Templates

Pandoc reads these fields from a YAML block at the top of your Markdown file. For example:

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

When you run md2ltx:

    md2ltx my_document.md --template=two-column-article

Pandoc loads the chosen “two-column-article” template, substitutes $title$, $author$, $date$, and $body$, and then compiles a PDF. The same process applies to any of the provided templates.

---------------------------------------------------------------------------------

## 3. Embedded Python Code with `<e{ … }e>`

md2ltx also supports executing small Python code blocks inline with your Markdown, then replacing those blocks with the code’s return value. This is done via special tags in your Markdown:

    <e{
    # Python code here
    }e>

### 3.1. Requirements

• You must define exactly one function named `evaluate()`, which returns a string.  
• No need to call `evaluate()` yourself; md2ltx will call it automatically.  
• Any leading or trailing whitespace in the returned string is trimmed.  
• Access to certain libraries are available in the `<e{ ... }e>` Python environment (math, pandas as pd, numpy as np, rgwfuncs) and do not need to be imported.

### 3.2. Example Usage

Suppose you want to compute the square root of 16 using the math library:

    <e{
    def my_result() -> str:
        val = math.sqrt(16)
        return f"The square root of 16 is {val}"
    }e>

When md2ltx processes this Markdown, it will:  

1. Extract the Python code between `<e{ and }e>`.  
2. Execute it in an environment where math, pd, np, and rgwfuncs are already available.  
3. Call `evaluate()` for you.  
4. Replace the entire `<e{ … }e>` block in the final PDF with the string returned by my_result().  

So, in the final PDF, you’ll see:

    The square root of 16 is 4.0

### 3.3. Another Example (Pandas, Numpy)

    <e{
    def my_result() -> str:
        data = np.array([1,2,3,4])
        s = pd.Series(data)
        mean_val = s.mean()
        return f"The mean of [1,2,3,4] is {mean_val}"
    }e>

Here, we use numpy arrays `np.array()`, and a pandas Series `pd.Series`. md2ltx automatically provides np and pd in the environment without requiring separate imports.

--------------------------------------------------------------------------------

## 4. General Pandoc Tranformations

md2ltx uses Pandoc to transform Markdown files into LaTeX, which pdflatex then uses to generate a final PDF. This workflow supports most of Markdown’s core syntax plus many Pandoc extensions. Below is a high-level overview of how Pandoc typically converts various Markdown constructs into LaTeX. For full details, refer to Pandoc’s official documentation.

---

### 4.1. Headings

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

### 4.2. Emphasis &amp; Strong Emphasis

• <strong>Markdown</strong>  
  <pre><code>*emphasis* or _emphasis_  
**strong emphasis** or __strong emphasis__</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\emph{emphasis}  
\textbf{strong emphasis}</code></pre>

---

### 4.3. Inline Code

• <strong>Markdown</strong>  
  <pre><code>`inline code`</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\texttt{inline code}</code></pre>

---

### 4.4. Code Blocks

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

### 4.5. Lists

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

### 4.6. Links &amp; Images

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

### 4.7. Blockquotes

• <strong>Markdown</strong>  
  <pre><code>> This is a blockquote.</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\begin{quote}  
This is a blockquote.  
\end{quote}</code></pre>

---

### 4.8. Horizontal Rules

• <strong>Markdown</strong>  
  <pre><code>---  
***  
___</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>\hrule</code></pre>

---

### 4.9. Footnotes (Pandoc Extension)

• <strong>Markdown</strong>  
  <pre><code>This is some text with a footnote.[^1]

[^1]: This is the footnote text.</code></pre>

• <strong>Pandoc → LaTeX</strong>  
  <pre><code>This is some text with a footnote.\footnote{This is the footnote text.}</code></pre>

---

### 4.10. Tables

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

### 4.11. Math &amp; LaTeX Blocks

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

### 4.12. Citations &amp; Bibliographies

Pandoc can handle citations if you provide a bibliography file. A reference like <code>[@smith2009]</code> can become <code>\cite{smith2009}</code> or <code>\autocite</code> depending on the style and Pandoc’s command-line options.

---

### 4.14. Raw LaTeX

Pandoc passes raw LaTeX through if you’re converting to LaTeX or PDF. For example:

```
\newpage
```

remains <code>\newpage</code> in the output.

---



"""
