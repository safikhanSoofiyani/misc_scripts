Translate the following Markdown document from English into {{TARGET_LANG_NAME}} ({{TARGET_LANG_CODE}}).

## What to translate
- All prose: paragraphs, sentences, blockquotes (`>`), list item text, and heading text.
- Alt text inside image tags: `![alt text](path)` → translate only the alt text, not the path.
- Link display text: `[display text](url)` → translate only the display text, not the URL.
- Bold/italic prose: `**word**`, `*word*` → translate the inner text, keep the markers.

## What to NEVER translate or modify
- Markdown syntax tokens: `#`, `##`, `###`, `-`, `*`, `>`, `|`, `---`, ` ``` `, `**`, `_`, etc.
- Inline code: anything inside single backticks `` `code` ``.
- Fenced code blocks: everything between ` ``` ` and ` ``` ` (including the fence lines).
- URLs and link targets: the `(url)` part of `[text](url)`.
- Image paths: the `(path)` part of `![alt](path)`.
- HTML tags if present (e.g. `<br>`, `<img>`, `<table>`).
- Any span listed under Protected Spans below.

## Formatting rules
- Preserve heading levels exactly (`#`, `##`, `###` etc.) — do not change hierarchy.
- Preserve blank lines between sections; do not merge or split paragraphs.
- Keep list markers (`-`, `*`, `1.`) unchanged; translate only the text that follows them.
- Return only the translated document — no commentary, no preamble.

Protected spans (copy byte-for-byte):
{{PROTECTED_SPANS}}

Additional translation notes:
{{TRANSLATION_NOTES}}

Source document:
{{SOURCE_TEXT}}
