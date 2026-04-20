Translate the following technical document from English into {{TARGET_LANG_NAME}} ({{TARGET_LANG_CODE}}).

This document mixes explanatory prose, code blocks, docstrings, and inline comments. Apply translation surgically: prose and human-readable explanations get translated; code and identifiers do not.

## What to translate
- Prose paragraphs outside code blocks: explanations, introductions, and summaries.
- Docstring body text inside `"""..."""` or `'''...'''` — translate the natural-language description, but preserve parameter names, types, return labels, and example code within the docstring.
- Inline code comments after `#` (Python/Shell/YAML), `//` (JS/Java/C), or `--` (SQL) — translate the comment text that follows the marker; keep the marker itself.
- Section headings and callout text that are clearly prose.

## What to NEVER translate or modify
- Anything inside a fenced code block (between ` ``` ` and ` ``` `) — copy byte-for-byte.
- Inline code inside backticks `` `identifier` ``.
- Function names, variable names, class names, method names, and identifiers anywhere.
- Import statements, package names, module paths.
- Shell commands, flags, and arguments (e.g. `git commit -m`, `pip install`).
- SQL keywords, table names, column names, and query structure.
- YAML/JSON keys and values that are configuration identifiers or enum strings.
- URLs, file paths, environment variable names.
- Any span listed under Protected Spans below.

## Docstring translation example
Original:
```python
def compute_loss(predictions, labels):
    """
    Compute cross-entropy loss between predictions and ground truth labels.

    Args:
        predictions: Tensor of shape (N, C) with raw logits.
        labels: Tensor of shape (N,) with integer class indices.

    Returns:
        Scalar loss value.
    """
```
Correct output (Hindi example — adapt for {{TARGET_LANG_NAME}}):
```python
def compute_loss(predictions, labels):
    """
    predictions और ground truth labels के बीच cross-entropy loss की गणना करता है।

    Args:
        predictions: आकार (N, C) का Tensor जिसमें raw logits हैं।
        labels: आकार (N,) का Tensor जिसमें integer class indices हैं।

    Returns:
        Scalar loss value।
    """
```
Note: function name, argument names, types, and shape annotations are untouched.

## Formatting rules
- Keep fenced code block language tags (e.g. ` ```python `, ` ```bash `).
- Preserve indentation inside and outside code blocks exactly.
- Return only the translated document — no commentary, no preamble.

Protected spans (copy byte-for-byte):
{{PROTECTED_SPANS}}

Additional translation notes:
{{TRANSLATION_NOTES}}

Source document:
{{SOURCE_TEXT}}
