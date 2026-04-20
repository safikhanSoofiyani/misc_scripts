Translate the following document (which contains tables and image references) from English into {{TARGET_LANG_NAME}} ({{TARGET_LANG_CODE}}).

## What to translate
- All narrative prose: paragraphs, section introductions, and concluding remarks.
- Table header cells and table data cells that contain natural-language text.
- Image captions and figure descriptions.
- Alt text inside image tags: `![alt text](path)` → translate only the alt text.
- Link display text: `[display text](url)` → translate only the display text, not the URL.

## What to NEVER translate or modify
- Image file paths and URLs: the `(path)` or `(url)` portion of Markdown image/link syntax.
- HTML `src`, `href`, or `alt` attribute values that are file paths or URLs.
- Table structure characters: `|`, `-`, `:` alignment markers.
- Numeric values, units, percentages, and measurement data inside table cells.
- Product codes, SKUs, identifiers, or technical IDs in any cell.
- Any span listed under Protected Spans below.

## Formatting rules
- Keep every table row and column intact — do not add, remove, or merge cells.
- Preserve the alignment row (`|---|---|`) exactly as-is.
- Keep Markdown image syntax `![alt](path)` — only the alt text changes.
- Return only the translated document — no commentary, no preamble.

Protected spans (copy byte-for-byte):
{{PROTECTED_SPANS}}

Additional translation notes:
{{TRANSLATION_NOTES}}

Source document:
{{SOURCE_TEXT}}
