import json
import re
from typing import List

import datasets


FEW_SHOT_PATH = (
    "/lustre/fsw/portfolios/sw/users/kipraveen/workspace/nemotron4_utils/"
    "lm_evaluation_harness/extras/jeebench/data/few_shot_examples.json"
)

with open(FEW_SHOT_PATH) as f:
    FEW_SHOT_EXAMPLES = json.load(f)


def _process_docs(dataset: datasets.Dataset, subject: str) -> datasets.Dataset:
    def _filter(doc):
        return doc["type"] == "MCQ" and doc["subject"] == subject

    def _augment(doc):
        doc["answer"] = "ABCD".index(doc["gold"])
        return doc

    return dataset.filter(_filter).map(_augment)


def process_docs_phy(dataset: datasets.Dataset) -> datasets.Dataset:
    return _process_docs(dataset, "phy")


def process_docs_chem(dataset: datasets.Dataset) -> datasets.Dataset:
    return _process_docs(dataset, "chem")


def process_docs_math(dataset: datasets.Dataset) -> datasets.Dataset:
    return _process_docs(dataset, "math")


def _fewshot_for(subject: str) -> List[dict]:
    ex = FEW_SHOT_EXAMPLES[subject]["MCQ"]
    gold = re.search(r"\\boxed\{([A-D])\}", ex["solution"]).group(1)
    return [
        {
            "question": ex["problem"],
            "gold": gold,
            "answer": "ABCD".index(gold),
            "type": "MCQ",
            "subject": subject,
            "description": "few_shot",
            "index": -1,
        }
    ]


def list_fewshot_samples_phy() -> List[dict]:
    return _fewshot_for("phy")


def list_fewshot_samples_chem() -> List[dict]:
    return _fewshot_for("chem")


def list_fewshot_samples_math() -> List[dict]:
    return _fewshot_for("math")
