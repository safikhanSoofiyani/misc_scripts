Evaluate the candidate translation from English into {{TARGET_LANG_NAME}} ({{TARGET_LANG_CODE}}).

Document style: {{STYLE_LABEL}}
Style description: {{STYLE_DESCRIPTION}}

Focus areas for this style:
{{STYLE_JUDGE_FOCUS}}

Protected spans that should remain unchanged:
{{PROTECTED_SPANS}}

Deterministic checks already computed:
{{AUTOMATIC_CHECKS_JSON}}

Scoring rubric:
- `faithfulness`: meaning preservation and completeness.
- `fluency`: naturalness and readability in the target language.
- `terminology`: correct technical, academic, or domain-specific term choice.
- `format_preservation`: structure, markup, tables, code fences, LaTeX, and layout preservation.
- `protected_span_handling`: correct copying of protected spans without accidental translation or corruption.
- `style_specific_quality`: how well the translation meets the style-specific demands of this document type.

Overall score instructions:
- Convert the six 0-5 dimension scores into a 0-100 overall score.
- Use these weights: faithfulness 30, fluency 20, terminology 15, format_preservation 15, protected_span_handling 10, style_specific_quality 10.
- If protected spans are corrupted or deterministic checks show clear structural breakage, cap the overall score at 59.
- Set `passed` to `true` only if overall_score >= 75 and faithfulness >= 4 and format_preservation >= 4.

Return exactly one JSON object with this schema:
{
  "dimension_scores": {
    "faithfulness": 0-5,
    "fluency": 0-5,
    "terminology": 0-5,
    "format_preservation": 0-5,
    "protected_span_handling": 0-5,
    "style_specific_quality": 0-5
  },
  "overall_score": 0-100,
  "passed": true,
  "strengths": ["short point", "short point"],
  "issues": ["short point", "short point"],
  "summary": "one short paragraph"
}

Source document:
{{SOURCE_TEXT}}

Candidate translation:
{{TRANSLATION_TEXT}}
