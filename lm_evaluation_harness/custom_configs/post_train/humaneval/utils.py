import evaluate as hf_evaluate
import os
import re

os.environ["HF_ALLOW_CODE_EVAL"] = "1" 


try:
    compute_ = hf_evaluate.load("code_eval")
    test_cases = ["assert add(2, 3)==5"]
    candidates = [["def add(a,b): return a*b"]]
    results = compute_.compute(references=test_cases, predictions=candidates, k=[1])
except Exception as e:
    raise e


def pass_at_k(references: list[str], predictions: list[list[str]], k: list[int] = None):
    global compute_
    assert k is not None
    if isinstance(k, int):
        k = [k]
    res = compute_.compute(
        references=references,
        predictions=predictions,
        k=k,
    )
    return res[0]


def build_predictions(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_assamese(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Assamese_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_bengali(resps, docs):
    return [[doc["prompt_Bengali_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_bodo(resps, docs):
    return [[doc["prompt_Bodo_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_dogri(resps, docs):
    return [[doc["prompt_Dogri_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_gujarati(resps, docs):
    return [[doc["prompt_Gujarati_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_hindi(resps, docs):
    return [[doc["prompt_Hindi_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_kannada(resps, docs):
    return [[doc["prompt_Kannada_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_kashmiri(resps, docs):
    return [[doc["prompt_Kashmiri_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_konkani(resps, docs):
    return [[doc["prompt_Konkani_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_maithili(resps, docs):
    return [[doc["prompt_Maithili_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_malayalam(resps, docs):
    return [[doc["prompt_Malayalam_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_manipuri(resps, docs):
    return [[doc["prompt_Manipuri_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_marathi(resps, docs):
    return [[doc["prompt_Marathi_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_nepali(resps, docs):
    return [[doc["prompt_Nepali_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_odiya(resps, docs):
    return [[doc["prompt_Odiya_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_punjabi(resps, docs):
    return [[doc["prompt_Punjabi_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_sanskrit(resps, docs):
    return [[doc["prompt_Sanskrit_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_santali(resps, docs):
    return [[doc["prompt_Santali_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_sindhi(resps, docs):
    return [[doc["prompt_Sindhi_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_tamil(resps, docs):
    return [[doc["prompt_Tamil_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_telugu(resps, docs):
    return [[doc["prompt_Telugu_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_urdu(resps, docs):
    return [[doc["prompt_Urdu_translation"] + r for r in resp] for resp, doc in zip(resps, docs)]


# def build_predictions_instruct(
#     resps: list[list[str]], docs: list[dict]
# ) -> list[list[str]]:
#     return [
#         [
#             doc["prompt"] + (r if r.rfind("```") == -1 else r[: r.rfind("```")])
#             for r in resp
#         ]
#         for resp, doc in zip(resps, docs)
#     ]

def build_predictions_instruct(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    final_responses = []
    for resp in resps:
        resp_cleaned = []
        for r in resp:
            pattern = r'```(?:\w+)?\n(.*?)```'
            matches = re.findall(pattern, r, re.DOTALL)
            if not matches:
                resp_cleaned.append(r)
                continue
            code = matches[0]
            resp_cleaned.append(code)
        final_responses.append(resp_cleaned)
    return [[r for r in resp] for resp, doc in zip(final_responses, docs)]


def build_predictions_instruct_assamese(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Assamese_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_bengali(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Bengali_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_bodo(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Bodo_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_dogri(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Dogri_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_gujarati(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Gujarati_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_hindi(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Hindi_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_kannada(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Kannada_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_kashmiri(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Kashmiri_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_konkani(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Konkani_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_maithili(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Maithili_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_malayalam(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Malayalam_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_manipuri(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Manipuri_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_marathi(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Marathi_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_nepali(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Nepali_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_odiya(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Odiya_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_punjabi(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Punjabi_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_sanskrit(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Sanskrit_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_santali(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Santali_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_sindhi(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Sindhi_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_tamil(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Tamil_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_telugu(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Telugu_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]

def build_predictions_instruct_urdu(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
    return [[doc["prompt_Urdu_translation"] + (r if r.rfind("```") == -1 else r[:r.rfind("```")]) for r in resp] for resp, doc in zip(resps, docs)]
