Translate the following document from English into {{TARGET_LANG_NAME}} ({{TARGET_LANG_CODE}}).

This document contains embedded non-English spans (Hindi phrases, quoted utterances, glossary entries, or script examples) that must NOT be translated. Your job is to translate only the English portions.

## What to translate
- All English prose: sentences, paragraphs, headings, explanations, and instructions.
- English labels or framing text around embedded non-English spans (e.g. "The phrase X means..." — translate the English frame, leave X untouched).

## What to NEVER translate or modify
- Any Hindi text, Devanagari script, or other non-English embedded spans — copy them byte-for-byte into the output at the exact same position.
- Any span listed under Protected Spans below — these must appear in the output unchanged, in the same location relative to the surrounding translated text.
- Quoted utterances or glossary entries that are explicitly presented as examples in the source language.
- Transliterated words presented as vocabulary items (e.g. "namaste", "chai").

## How to handle embedded spans
- Translate the English sentence up to the embedded span.
- Insert the embedded span exactly as it appears in the source.
- Continue translating the remaining English text.
- Do not add quotation marks, brackets, or annotations around the preserved span.

## Formatting rules
- Preserve paragraph breaks, heading levels, and list structure.
- Return only the translated document — no commentary, no preamble.

Protected spans (copy byte-for-byte):
{{PROTECTED_SPANS}}

Additional translation notes:
{{TRANSLATION_NOTES}}

Source document:
{{SOURCE_TEXT}}
