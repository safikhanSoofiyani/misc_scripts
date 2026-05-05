import re
import string
import numpy as np

# Regex to strip leading/trailing whitespace & punctuation, and canonicalize casing
_ARTICLES = re.compile(r'\b(a|an|the)\b', re.UNICODE)


def normalize_answer(text):

    text = text.lower()
    text = _ARTICLES.sub(" ", text)
    text = ''.join(ch for ch in text if ch not in string.punctuation)
    text = " ".join(text.split())
    return (text.strip(),)

def extract_answer(text):
    extracted_text = text.lower().split("hence the answer is:")
    if len(extracted_text) > 1:
        answer = extracted_text[1].strip()
        return answer
    else:
        return ""
    

def process_results(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    max_em, max_f1 = 0.0, 0.0
    answers = [normalize_answer(ans) for ans in set(doc["answer_list"])]
    
    for gold in answers:
        gold = gold[0]
        em, f1 = get_metrics(pred, gold)
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)

    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_assamese(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Assamese_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_bengali(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Bengali_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_bodo(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Bodo_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_dogri(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Dogri_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_gujarati(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Gujarati_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_hindi(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Hindi_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_kannada(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Kannada_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_kashmiri(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Kashmiri_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_konkani(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Konkani_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_maithili(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Maithili_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_malayalam(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Malayalam_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_manipuri(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Manipuri_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_marathi(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Marathi_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_nepali(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Nepali_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_odiya(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Odiya_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_punjabi(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Punjabi_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_sanskrit(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Sanskrit_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_santali(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Santali_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_sindhi(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Sindhi_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_tamil(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Tamil_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_telugu(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Telugu_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_urdu(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Urdu_translation"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}

def process_results_assamese_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Assamese_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_bengali_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Bengali_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_gujarati_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Gujarati_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_hindi_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Hindi_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_kannada_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Kannada_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_malayalam_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Malayalam_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_marathi_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Marathi_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_nepali_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Nepali_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_odiya_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Odiya_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_punjabi_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Punjabi_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_sanskrit_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Sanskrit_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_tamil_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Tamil_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_telugu_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Telugu_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def process_results_urdu_roman(doc, results):
    pred = normalize_answer(extract_answer(results[0]))[0]
    answers = [normalize_answer(ans) for ans in set(doc["answer_list_Urdu_romanization"])]
    max_em, max_f1 = 0.0, 0.0
    for gold in answers:
        em, f1 = get_metrics(pred, gold[0])
        max_em = max(max_em, em)
        max_f1 = max(max_f1, f1)
    return {"em": max_em, "f1": round(max_f1, 2)}


def get_metrics(predicted, gold):
    p_tokens = set(predicted.split())
    g_tokens = set(gold.split())
    exact_match = 1.0 if p_tokens == g_tokens and len(p_tokens)==len(g_tokens) else 0.0
    if p_tokens or g_tokens:
        inter = len(p_tokens & g_tokens)
        prec = inter / len(p_tokens) if p_tokens else 1.0
        rec = inter / len(g_tokens) if g_tokens else 1.0
        f1 = (2*prec*rec)/(prec+rec) if prec+rec>0 else 0.0
    else:
        f1 = 1.0
    return exact_match, f1
