import re
from typing import Union

import evaluate as hf_evaluate


try:
    pass_at_k = hf_evaluate.load("code_eval")

    # run simple test to check code execution is enabled before model generation
    test_cases = ["assert add(2, 3)==5"]
    candidates = [["def add(a,b): return a*b"]]
    results = pass_at_k.compute(references=test_cases, predictions=candidates, k=[1])
except Exception as e:
    raise e


def pass_at_1(
    references: Union[str, list[str]], predictions: Union[str, list[list[str]]]
) -> float:
    if isinstance(references, str):
        references = [references]
    if isinstance(predictions[0], str):
        predictions = [[p] for p in predictions]
    return pass_at_k.compute(
        references=references,
        predictions=predictions,
        k=[1],
    )[0]["pass@1"]


def extract_code_blocks(text: str) -> str:
    # Pattern to match ```...``` blocks
    pattern = r"```(?:\w+)?\n?(.*?)\n?```"
    # (+ ```) as we add the opening "```python" to the gen_prefix
    matches = re.findall(pattern, r"```" + text, re.DOTALL)
    # if no matches, try to match ```...``` blocks (after removing the language)
    if not matches:
        text_without_lang = re.sub(r"```python", "```", text)
        matches = re.findall(pattern, text_without_lang, re.DOTALL)
    if not matches:
        return ""
    else:
        return matches[0]


# def build_predictions(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
#     return [[extract_code_blocks(r) for r in resp] for resp in resps]

def build_predictions(resps: list[list[str]], docs: list[dict]) -> list[list[str]]:
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


def list_fewshot_samples():
    return [
        {
            "task_id": 2,
            "question": "Write a function to find the similar elements from the given two tuple lists.",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question": "Write a python function to identify non-prime numbers.",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question": "Write a function to find the largest integers from a given list of numbers using heap queue algorithm.",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]

def list_fewshot_samples_assamese():
    return [
        {
            "task_id": 2,
            "question_Assamese_translation": "দিয়া থকা দুটা টিউপল তালিকাৰ পৰা একে উপাদানসমূহ বিচাৰি উলিয়াবলৈ এটা ফাংচন লিখা।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Assamese_translation": "অপ্ৰাইম সংখ্যা চিনাক্ত কৰিবলৈ এটা পাইথন ফাংচন লিখা।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Assamese_translation": "হিপ কিউ এলগৰিদম ব্যৱহাৰ কৰি এটা দিয়া সংখ্যাৰ তালিকাৰ পৰা আটাইতকৈ ডাঙৰ সংখ্যা বিচাৰি উলিয়াবলৈ এটা ফাংচন লিখা।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]

def list_fewshot_samples_bengali():
    return [
        {
            "task_id": 2,
            "question_Bengali_translation": "প্রদত্ত দুটি টুপল তালিকা থেকে মিল থাকা উপাদানগুলো খুঁজে বের করার জন্য একটি ফাংশন লিখুন।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Bengali_translation": "অপ্রাইম সংখ্যা চিহ্নিত করার জন্য একটি পাইথন ফাংশন লিখুন।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Bengali_translation": "হিপ কিউ অ্যালগরিদম ব্যবহার করে একটি তালিকা থেকে সবচেয়ে বড় সংখ্যা খুঁজে বের করার জন্য একটি ফাংশন লিখুন।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_bodo():
    return [
        {
            "task_id": 2,
            "question_Bodo_translation": "दिया गया दुई ट्यूपल लिस्ट से समान तत्व निकालै के फाङ्सन लिख।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Bodo_translation": "नन-प्राइम नम्बार चिन्हित करै फाङ्सन लिख।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Bodo_translation": "हीप क्यू एल्गोरिदम सायता लेकै सब सानथि डांगर नम्बार निकालै फाङ्सन लिख।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]



def list_fewshot_samples_dogri():
    return [
        {
            "task_id": 2,
            "question_Dogri_translation": "दिए गए दो ट्यूपल सूचियाँ विचों मिलद्या होया तत्व कढण वास्ते इक फंक्शन लिखो।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Dogri_translation": "नॉन-प्राइम नंबर्स नूं पहचानण वास्ते इक पाइथन फंक्शन लिखो।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Dogri_translation": "हीप क्यू एल्गोरिदम दा उपयोग करके सब तों वड्डे नंबर्स खोजण वास्ते फंक्शन लिखो।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_gujarati():
    return [
        {
            "task_id": 2,
            "tquestion_Gujarati_translationext": "આપેલ બે ટ્યુપલ સૂચિઓમાંથી સમાન તત્વો શોધવા માટે ફંક્શન લખો.",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Gujarati_translation": "પ્રાઇમ નંબર ન હોય તેવા નંબરો ઓળખવા માટે પાઈથન ફંક્શન લખો.",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Gujarati_translation": "હિપ ક્યુ એલ્ગોરિધમનો ઉપયોગ કરીને સંખ્યાઓની સૂચિમાંથી સૌથી મોટી સંખ્યાઓ શોધવા માટે ફંક્શન લખો.",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]
    

def list_fewshot_samples_hindi():
    return [
        {
            "task_id": 2,
            "question_Hindi_translation": "दो दी गई ट्यूपल सूचियों से समान तत्वों को खोजने के लिए एक फ़ंक्शन लिखिए।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Hindi_translation": "गैर-मौलिक (नॉन-प्राइम) संख्याओं की पहचान करने के लिए एक पायथन फ़ंक्शन लिखिए।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Hindi_translation": "हीप क्यू एल्गोरिदम का उपयोग करके संख्याओं की सूची से सबसे बड़ी संख्याएँ खोजने के लिए एक फ़ंक्शन लिखिए।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_kannada():
    return [
        {
            "task_id": 2,
            "question_Kannada_translation": "ನೀಡಲಾದ ಎರಡು ಟ್ಯೂಪಲ್ ಪಟ್ಟಿಗಳಲ್ಲಿ ಒಂದೇ ಆದ ಅಂಶಗಳನ್ನು ಕಂಡುಹಿಡಿಯುವ ಫಂಕ್ಷನ್ ಅನ್ನು ಬರೆಯಿರಿ.",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Kannada_translation": "ಅಪರಿಮಿತ ಸಂಖ್ಯೆಗಳನ್ನು ಗುರುತಿಸಲು ಪೈಥಾನ್ ಫಂಕ್ಷನ್ ಅನ್ನು ಬರೆಯಿರಿ.",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Kannada_translation": "ಹೀಪ್ ಕ್ಯೂ الگಾರಿದಮ್ ಉಪಯೋಗಿಸಿ ಸಂಖ್ಯೆಗಳ ಪಟ್ಟಿಯಿಂದ ಅತಿದೊಡ್ಡ ಸಂಖ್ಯೆಗಳನ್ನು ಹುಡುಕುವ ಫಂಕ್ಷನ್ ಅನ್ನು ಬರೆಯಿರಿ.",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]
    
    
def list_fewshot_samples_kashmiri():
    return [
        {
            "task_id": 2,
            "question_Kashmiri_translation": "دوٗن دِیہ گٔے ٹیوپل فہرستن منز یکسان عُنصر تلاش کرنہ وَسٹہ ایک فَنکشن لِکھِو۔",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Kashmiri_translation": "نَن پرائم نمبر پَہچاننہ وَسٹہ ایک پائتھن فَنکشن لِکھِو۔",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Kashmiri_translation": "ہیپ کیو الگورِدم استعمال کرِتھ بڈ نمبرنہ تلاش کرنہ وَسٹہ ایک فَنکشن لِکھِو۔",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_konkani():
    return [
        {
            "task_id": 2,
            "question_Konkani_translation": "दोन दिल्ल्या ट्युपल लिस्टांतलें सारखें घटक सापडोवपाचेर फंक्शन लिहा.",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Konkani_translation": "नॉन-प्राइम नंबर ओळखपाचेर एक पायथन फंक्शन लिहा.",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Konkani_translation": "हीप क्यू अल्गोरिदम वापरून दिल्ल्या लिस्टांतलें सगळ्यांत मोठे नंबर शोधपाचेर फंक्शन लिहा.",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_maithili():
    return [
        {
            "task_id": 2,
            "question_Maithili_translation": "दू गो दिअल ट्यूपल सूची स मिलैत तत्व सभ के पता लगाबै वाला एकटा फंक्शन लिखू।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Maithili_translation": "गैर-प्राइम संख्या के चिन्हित करै बाला एकटा पाइथन फंक्शन लिखू।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Maithili_translation": "हीप क्यू एल्गोरिद्म के उपयोग स संख्या सभक सूची स सबसे पैघ संख्या पता लगाबै बला फंक्शन लिखू।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_malayalam():
    return [
        {
            "task_id": 2,
            "question_Malayalam_translation": "നല്‍കിയ രണ്ട് ട്യൂപ്പിള്‍ ലിസ്റ്റുകളില്‍ നിന്നും ഒരേ ഘടകങ്ങള്‍ കണ്ടെത്താനുള്ള ഒരു ഫംഗ്ഷന്‍ എഴുതുക.",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Malayalam_translation": "പ്രൈം അല്ലാത്ത സംഖ്യകള്‍ തിരിച്ചറിയുന്നതിനായി ഒരു പൈത്തണ്‍ ഫംഗ്ഷന്‍ എഴുതുക.",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Malayalam_translation": "ഹീപ് ക്യൂ ആല്‍ഗോരിതം ഉപയോഗിച്ച് ഒരു ലിസ്റ്റില്‍ നിന്നുള്ള ഏറ്റവും വലിയ സംഖ്യകള്‍ കണ്ടെത്താനുള്ള ഫംഗ്ഷന്‍ എഴുതുക.",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]

def list_fewshot_samples_manipuri():
    return [
        {
            "task_id": 2,
            "question_Manipuri_translation": "ꯗꯨꯂꯥ ꯗꯤꯌꯥ ꯇꯨꯄꯜ ꯂꯤꯁ꯭ꯇꯔꯦꯡ ꯐꯪ ꯑꯃꯨꯡ ꯊꯥꯏ ꯊꯥꯡꯗ ꯌꯥꯝꯅꯕ ꯑꯃꯨ ꯐꯥꯪꯁꯟ ꯂꯤꯈꯣꯛ।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Manipuri_translation": "ꯅꯣꯟ-ꯄ꯭ꯔꯥꯏꯝ ꯑꯁꯤ ꯁꯦꯝꯀꯌꯥ ꯑꯁꯤꯡ ꯊꯥꯏ ꯊꯥꯡꯗ ꯌꯥꯝꯅꯕ ꯑꯃꯨ ꯄꯥꯏꯊꯟ ꯐꯥꯪꯁꯟ ꯂꯤꯈꯣꯛ।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Manipuri_translation": "ꯍꯤꯞ ꯀꯨ ꯑꯜꯒꯣꯔꯤꯗꯝ ꯑꯃꯨ ꯌꯥꯝꯅꯕ ꯁꯦꯝꯀꯌꯥ ꯁꯨꯖꯤꯒꯤ ꯑꯁꯤꯡ ꯂꯣꯜꯂꯨ ꯑꯃꯨ ꯐꯥꯪꯁꯟ ꯂꯤꯈꯣꯛ।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_marathi():
    return [
        {
            "task_id": 2,
            "question_Marathi_translation": "दिलेल्या दोन ट्युपल याद्यांमधून समान घटक शोधण्यासाठी एक फंक्शन लिहा.",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Marathi_translation": "नॉन-प्राइम (अविभाज्य नसलेले) नंबर ओळखण्यासाठी एक पायथन फंक्शन लिहा.",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Marathi_translation": "हीप क्यू अल्गोरिदम वापरून संख्या यादीतून सर्वात मोठ्या संख्यांचा शोध घेण्यासाठी फंक्शन लिहा.",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_nepali():
    return [
        {
            "task_id": 2,
            "question_Nepali_translation": "दिइएको दुईवटा ट्युपल सूचीबाट समान तत्वहरू फेला पार्ने कार्यका लागि एउटा फङ्सन लेख्नुहोस्।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Nepali_translation": "प्राइम नभएका सङ्ख्या पत्ता लगाउने पायथन फङ्सन लेख्नुहोस्।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Nepali_translation": "हीप क्यू एल्गोरिदम प्रयोग गरेर सबैभन्दा ठूलो सङ्ख्या खोज्ने फङ्सन लेख्नुहोस्।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_odiya():
    return [
        {
            "task_id": 2,
            "question_Odiya_translation": "ଦିଆଯାଇଥିବା ଦୁଇଟି ଟ୍ୟୁପଲ ତାଲିକାରୁ ସମାନ ଉପାଦାନ ଚିହ୍ନଟ କରିବା ପାଇଁ ଏକ ଫଙ୍କସନ୍ ଲେଖ।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Odiya_translation": "ଅପ୍ରାଇମ ସଂଖ୍ୟାଗୁଡ଼ିକ ଚିହ୍ନଟ କରିବା ପାଇଁ ଏକ ପାଇଥନ୍ ଫଙ୍କସନ୍ ଲେଖ।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Odiya_translation": "ହିପ୍ କ୍ୟୁ ଏଲଗୋରିଦମ୍ ବ୍ୟବହାର କରି ସବୁଠୁ ବଡ଼ ସଂଖ୍ୟାଗୁଡ଼ିକ ଚିହ୍ନଟ କରିବା ପାଇଁ ଏକ ଫଙ୍କସନ୍ ଲେଖ।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_punjabi():
    return [
        {
            "task_id": 2,
            "question_Punjabi_translation": "ਦਿੱਤੀਆਂ ਹੋਈਆਂ ਦੋ ਟਿਊਪਲ ਸੂਚੀਆਂ ਵਿੱਚੋਂ ਇੱਕੋ ਜਿਹੇ ਤੱਤ ਲੱਭਣ ਲਈ ਇੱਕ ਫੰਕਸ਼ਨ ਲਿਖੋ।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Punjabi_translation": "ਨਾ-ਪ੍ਰਾਈਮ ਨੰਬਰ ਪਛਾਣਣ ਲਈ ਇੱਕ ਪਾਇਥਨ ਫੰਕਸ਼ਨ ਲਿਖੋ।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Punjabi_translation": "ਹੀਪ ਕਿਊ ਐਲਗੋਰਿਦਮ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਸਭ ਤੋਂ ਵੱਡੇ ਨੰਬਰ ਲੱਭਣ ਲਈ ਇੱਕ ਫੰਕਸ਼ਨ ਲਿਖੋ।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_sanskrit():
    return [
        {
            "task_id": 2,
            "question_Sanskrit_translation": "दत्तयोः द्वयोः ट्युपल-सूच्योः समानानि अवयवानि ज्ञातुं एकं कार्यक्रमं लिखत।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Sanskrit_translation": "अप्रधानसंख्यानि ज्ञातुं एकं पाइथन् कार्यक्रमं लिखत।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Sanskrit_translation": "हीप्-क्यू नामक-संगणक-क्रमणिका प्रयोग्य सूच्याः शीर्षाणि संख्यानि ज्ञातुं कार्यक्रमं लिखत।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_santali():
    return [
        {
            "task_id": 2,
            "question_Santali_translation": "ᱫᱤᱭᱟ ᱞᱮᱛᱟ ᱛᱷᱟᱹ ᱴᱼᱩᱯᱞ ᱠᱟᱛᱮ ᱞᱤᱥᱴ ᱠᱚ ᱴᱮᱵᱟᱨ ᱵᱟᱝ ᱦᱚᱸᱫᱟ ᱟᱢ ᱪᱮ ᱯᱟᱹᱨᱥᱤ ᱯᱚᱞ ᱪᱟᱹᱛᱤ ᱞᱮᱠᱷ।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Santali_translation": "ᱱᱚᱱ-ᱯᱨᱟᱭᱢ ᱥᱟᱝᱠᱤ ᱠᱚ ᱦᱚᱸᱫᱟ ᱟᱢ ᱯᱟᱹᱨᱥᱤ ᱯᱚᱞ ᱪᱟᱹᱛᱤ ᱞᱮᱠᱷ।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Santali_translation": "ᱦᱤᱯ ᱠᱩ ᱟᱞᱜᱚᱨᱤᱰᱟᱢ ᱮᱢ ᱥᱟᱝᱠᱤ ᱥᱩᱪᱤ ᱠᱚ ᱵᱚᱫᱚ ᱦᱚᱸᱫᱟ ᱟᱢ ᱯᱟᱹᱨᱥᱤ ᱯᱚᱞ ᱪᱟᱹᱛᱤ ᱞᱮᱠᱷ।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]

def list_fewshot_samples_sindhi():
    return [
        {
            "task_id": 2,
            "question_Sindhi_translation": "दिईल व‌या ट्यूपल सूचियन में एकसरखं घटक वठन ला एक फंक्शन लिखो।",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Sindhi_translation": "नॉन-प्राइम नंबर जो पहचान करन ला एक पायथन फंक्शन लिखो।",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Sindhi_translation": "हीप क्यू एल्गोरिदम जो उपयोग करि वडां नंबर वठन ला एक फंक्शन लिखो।",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_tamil():
    return [
        {
            "task_id": 2,
            "question_Tamil_translation": "கொடுக்கப்பட்ட இரண்டு ட்யூபிள் பட்டியல்களில் இருந்து ஒரே போன்ற கூறுகளை கண்டறிய ஒரு செயலியை எழுதுங்கள்.",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Tamil_translation": "பிரைம் எண்கள் அல்லாத எண்களை கண்டறிய ஒரு பைதான் செயலியை எழுதுங்கள்.",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Tamil_translation": "ஹீப் க்யூ அல்கோரிதத்தை பயன்படுத்தி மிகப்பெரிய எண்களை கண்டறிய ஒரு செயலியை எழுதுங்கள்.",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_telugu():
    return [
        {
            "task_id": 2,
            "question_Telugu_translation": "ఇచ్చిన రెండు ట్యూపుల్ జాబితాల్లో ఉన్న సమానమైన అంశాలను కనుగొనడానికి ఒక ఫంక్షన్‌ను రాయండి.",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Telugu_translation": "ప్రైమ్ కాని సంఖ్యలను గుర్తించేందుకు పాథాన్ ఫంక్షన్‌ను రాయండి.",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Telugu_translation": "హీప్ క్యూలు అల్గోరిథంను ఉపయోగించి ఇచ్చిన జాబితా నుండి అత్యధిక సంఖ్యలను కనుగొనండి.",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]


def list_fewshot_samples_urdu():
    return [
        {
            "task_id": 2,
            "question_Urdu_translation": "دی گئی دو ٹیوپل فہرستوں میں سے ایک جیسے عناصر تلاش کرنے کے لیے ایک فنکشن لکھیں۔",
            "code": "def similar_elements(test_tup1, test_tup2):\r\n  res = tuple(set(test_tup1) & set(test_tup2))\r\n  return (res) ",
            "test_list": [
                "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
                "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
                "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 3,
            "question_Urdu_translation": "غیر اولیہ (نَن پرائم) اعداد کو پہچاننے کے لیے ایک پائتھن فنکشن لکھیں۔",
            "code": "import math\r\ndef is_not_prime(n):\r\n    result = False\r\n    for i in range(2,int(math.sqrt(n)) + 1):\r\n        if n % i == 0:\r\n            result = True\r\n    return result",
            "test_list": [
                "assert is_not_prime(2) == False",
                "assert is_not_prime(10) == True",
                "assert is_not_prime(35) == True",
            ],
            "is_fewshot": True,
        },
        {
            "task_id": 4,
            "question_Urdu_translation": "ہیپ کیو الگوردم کا استعمال کرتے ہوئے سب سے بڑی اعداد تلاش کرنے کے لیے ایک فنکشن لکھیں۔",
            "code": "import heapq as hq\r\ndef heap_queue_largest(nums,n):\r\n  largest_nums = hq.nlargest(n, nums)\r\n  return largest_nums",
            "test_list": [
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75] ",
                "assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]",
            ],
            "is_fewshot": True,
        },
    ]
