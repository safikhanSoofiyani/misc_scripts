Translate the following LaTeX-formatted document from English into {{TARGET_LANG_NAME}} ({{TARGET_LANG_CODE}}).

## What to translate
- All English prose: sentences, paragraphs, captions, theorem labels (e.g. "Theorem", "Proof", "Remark", "Definition"), section headings, and inline explanations.
- Translatable text inside `\text{...}`, `\textbf{...}`, `\textit{...}`, `\caption{...}`, `\section{...}`, `\subsection{...}`, and similar commands where the argument is clearly a prose phrase.

## What to NEVER translate or modify
- All LaTeX math: inline math `$...$`, display math `\[...\]`, `$$...$$`, and equation environments (`\begin{equation}`, `\begin{align}`, `\begin{gather}`, etc.).
- LaTeX commands and macros: `\frac`, `\int`, `\sum`, `\begin`, `\end`, `\label`, `\ref`, `\cite`, `\newcommand`, `\usepackage`, and all backslash-prefixed tokens.
- Math symbols, Greek letters, and operators inside math mode.
- `\label{...}` arguments — these are identifiers, never prose.
- URL/file references inside `\href`, `\includegraphics`, etc.
- Any span listed under Protected Spans below — copy them byte-for-byte.

## Formatting rules
- Keep all LaTeX structure intact: environments, nesting, indentation.
- Do not add, remove, or reorder any LaTeX commands or math expressions.
- Return only the translated document — no commentary, no preamble, no fences.

Protected spans (copy byte-for-byte):
{{PROTECTED_SPANS}}

Additional translation notes:
{{TRANSLATION_NOTES}}

Source document:
{{SOURCE_TEXT}}
