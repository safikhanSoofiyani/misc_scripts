"""Utilities for the JEEBench evaluation task.

Builds CoT+OneShot prompts using subject- and type-specific few-shot examples
(from the original JEEBench repository) and scores generations using JEE-style
marking after extracting the final answer from the last ``\\boxed{...}`` span.
"""

import json
import re
from typing import Dict, List

import datasets


PROMPT_LIBRARY = {
    "MCQ": (
        "In this problem, only one option will be correct. "
        "Give a detailed solution and end the solution with the final answer."
    ),
    "MCQ(multiple)": (
        "In this problem, multiple options can be correct. "
        "Give a detailed solution and end the solution with the final answer."
    ),
    "Integer": (
        "In this problem, the final answer will be a non-negative integer. "
        "Give a detailed solution and end the solution with the final answer."
    ),
    "Numeric": (
        "In this problem, the final will be a numeric value. "
        "Give the numerical answer correct upto the 2nd decimal digit. "
        "Give a detailed solution and end the solution with the final answer."
    ),
}

FEW_SHOT_PATH = (
    "/lustre/fsw/portfolios/sw/users/kipraveen/workspace/nemotron4_utils/"
    "lm_evaluation_harness/extras/jeebench/data/few_shot_examples.json"
)

with open(FEW_SHOT_PATH) as f:
    FEW_SHOT_EXAMPLES = json.load(f)


def _filter_by_subject(dataset: datasets.Dataset, subject: str) -> datasets.Dataset:
    return dataset.filter(lambda doc: doc["subject"] == subject)


def process_docs_phy(dataset: datasets.Dataset) -> datasets.Dataset:
    return _filter_by_subject(dataset, "phy")


def process_docs_chem(dataset: datasets.Dataset) -> datasets.Dataset:
    return _filter_by_subject(dataset, "chem")


def process_docs_math(dataset: datasets.Dataset) -> datasets.Dataset:
    return _filter_by_subject(dataset, "math")


def doc_to_text(doc: dict) -> str:
    prefix_prompt = PROMPT_LIBRARY[doc["type"]]
    ex = FEW_SHOT_EXAMPLES[doc["subject"]][doc["type"]]
    stripped_ques = doc["question"].replace("\n\n", "\n").strip()
    return (
        prefix_prompt
        + "\n\nProblem: "
        + ex["problem"]
        + "\nSolution: "
        + ex["solution"]
        + "\n\nProblem: "
        + stripped_ques
        + "\nSolution: "
    )


def doc_to_target(doc: dict) -> str:
    return doc["gold"]


_BOXED_RE = re.compile(r"\\boxed\{([^{}]*)\}")
_FALLBACK_RE = re.compile(
    r"(?:the\s+answer\s+is|final\s+answer[:\s]*is|answer\s*:)\s*\$?([A-D]+|-?\d+(?:\.\d+)?)",
    flags=re.IGNORECASE,
)


def _extract_raw_answer(text: str) -> str:
    boxed = _BOXED_RE.findall(text)
    if boxed:
        return boxed[-1].strip()
    m = _FALLBACK_RE.search(text)
    return m.group(1).strip() if m else ""


def _extract_answer(text: str, question_type: str) -> str:
    raw = _extract_raw_answer(text)
    if not raw:
        return "None"
    if question_type in ("MCQ", "MCQ(multiple)"):
        letters = "".join(sorted({c for c in "ABCD" if c in raw}))
        return letters or "None"
    m = re.search(r"-?\d+(?:\.\d+)?", raw)
    return m.group(0) if m else "None"


def _compute_score(gold: str, resp: str, question_type: str) -> float:
    if question_type == "MCQ(multiple)":
        gold_set = {c for c in "ABCD" if c in gold}
        resp_set = {c for c in "ABCD" if c in resp}
        if resp_set == gold_set:
            return 1.0
        if resp_set and resp_set <= gold_set:
            return 0.25 * len(resp_set)
        return 0.0
    if question_type == "MCQ":
        gold_set = {c for c in "ABCD" if c in gold}
        resp_set = {c for c in "ABCD" if c in resp}
        return 1.0 if gold_set == resp_set else 0.0
    if resp == "None":
        return 0.0
    try:
        return 1.0 if abs(float(gold) - float(resp)) <= 0.01 else 0.0
    except (ValueError, TypeError):
        return 0.0


def process_results(doc: dict, results: List[str]) -> Dict[str, float]:
    text = results[0] if results else ""
    extracted = _extract_answer(text, doc["type"])
    score = _compute_score(doc["gold"], extracted, doc["type"])
    return {"exact_match": score}
