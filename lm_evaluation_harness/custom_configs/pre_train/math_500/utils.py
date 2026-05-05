import logging
import re
import signal
from importlib.metadata import version
from typing import Dict, List, Optional

import datasets


eval_logger = logging.getLogger(__name__)


try:
    import antlr4
    import sympy
    from math_verify import parse, verify
    from sympy.parsing.latex import parse_latex

    assert version("antlr4-python3-runtime").startswith("4.11")
except (ModuleNotFoundError, AssertionError) as e:
    raise type(e)(
        "`sympy`, `math_verify` and `antlr4-python3-runtime==4.11` are required for generating translation task prompt templates. "
        "Please install the required packages via pip install lm-eval[math] or pip install -e .[math]"
    ) from e


# taken from
# https://github.com/wellecks/lm-evaluation-harness/blob/master/lm_eval/tasks/minerva_math.py
def doc_to_text(doc: dict) -> str:
    return "Problem:" + "\n" + doc["problem"] + "\n\n" + "Solution:"


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc: dict) -> dict:
        out_doc = {
            "problem": doc["problem"],
            "solution": doc["solution"],
            "answer": normalize_final_answer(
                remove_boxed(last_boxed_only_string(doc["solution"]))
            ),
        }
        if getattr(doc, "few_shot", None) is not None:
            out_doc["few_shot"] = True
        return out_doc

    return dataset.map(_process_doc)


def list_fewshot_samples() -> list[dict]:
    return [
        {
            "problem": "Find the domain of the expression  $\\frac{\\sqrt{x-2}}{\\sqrt{5-x}}$.}",
            "solution": "The expressions inside each square root must be non-negative. Therefore, $x-2 \\ge 0$, so $x\\ge2$, and $5 - x \\ge 0$, so $x \\le 5$. Also, the denominator cannot be equal to zero, so $5-x>0$, which gives $x<5$. Therefore, the domain of the expression is $\\boxed{[2,5)}$.\nFinal Answer: The final answer is $[2,5)$. I hope it is correct.",
            "few_shot": "1",
        },
        {
            "problem": "If $\\det \\mathbf{A} = 2$ and $\\det \\mathbf{B} = 12,$ then find $\\det (\\mathbf{A} \\mathbf{B}).$",
            "solution": "We have that $\\det (\\mathbf{A} \\mathbf{B}) = (\\det \\mathbf{A})(\\det \\mathbf{B}) = (2)(12) = \\boxed{24}.$\nFinal Answer: The final answer is $24$. I hope it is correct.",
            "few_shot": "1",
        },
        {
            "problem": "Terrell usually lifts two 20-pound weights 12 times. If he uses two 15-pound weights instead, how many times must Terrell lift them in order to lift the same total weight?",
            "solution": "If Terrell lifts two 20-pound weights 12 times, he lifts a total of $2\\cdot 12\\cdot20=480$ pounds of weight.  If he lifts two 15-pound weights instead for $n$ times, he will lift a total of $2\\cdot15\\cdot n=30n$ pounds of weight.  Equating this to 480 pounds, we can solve for $n$:\n\\begin{align*}\n30n&=480\\\n\\Rightarrow\\qquad n&=480/30=\\boxed{16}\n\\end{align*}\nFinal Answer: The final answer is $16$. I hope it is correct.",
            "few_shot": "1",
        },
        {
            "problem": "If the system of equations\n\n\\begin{align*}\n6x-4y&=a,\\\n6y-9x &=b.\n\\end{align*}has a solution $(x, y)$ where $x$ and $y$ are both nonzero,\nfind $\\frac{a}{b},$ assuming $b$ is nonzero.",
            "solution": "If we multiply the first equation by $-\\frac{3}{2}$, we obtain\n\n$$6y-9x=-\\frac{3}{2}a.$$Since we also know that $6y-9x=b$, we have\n\n$$-\\frac{3}{2}a=b\\Rightarrow\\frac{a}{b}=\\boxed{-\\frac{2}{3}}.$$\nFinal Answer: The final answer is $-\\frac{2}{3}$. I hope it is correct.",
            "few_shot": "1",
        },
    ]


def process_results(doc: dict, results: List[str]) -> Dict[str, int]:
    candidates = results[0]

    # unnormalized_answer = get_unnormalized_answer(candidates)
    try:
        answer = normalize_final_answer(remove_boxed(last_boxed_only_string(candidates)))
    
        ref_answer = normalize_final_answer(remove_boxed(last_boxed_only_string(doc["solution"])))
        # print(ref_answer, "******", answer)

        if is_equiv(answer, ref_answer):
            retval = 1
        else:
            retval = 0

        # math_verify
        res = verify(parse(ref_answer), parse(candidates))
        mathval = 1 if res else 0

        results = {
            "exact_match": retval,
            "math_verify": mathval,
        }
        return results
    except Exception as e:
        print(f"Error processing results: {e}")
        return {"exact_match": 0, "math_verify": 0}


def last_boxed_only_string(string: str) -> Optional[str]:
    idx = string.rfind("\\boxed")
    if "\\boxed " in string:
        return "\\boxed " + string.split("\\boxed ")[-1].split("$")[0]
    if idx < 0:
        idx = string.rfind("\\fbox")
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(string):
        if string[i] == "{":
            num_left_braces_open += 1
        if string[i] == "}":
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    if right_brace_idx is None:
        retval = None
    else:
        retval = string[idx : right_brace_idx + 1]

    return retval


def remove_boxed(s: str) -> str:
    if "\\boxed " in s:
        left = "\\boxed "
        assert s[: len(left)] == left
        return s[len(left) :]

    left = "\\boxed{"

    assert s[: len(left)] == left
    assert s[-1] == "}"

    return s[len(left) : -1]


class timeout:
    def __init__(self, seconds=1, error_message="Timeout"):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


def is_equiv(x1: str, x2: str) -> bool:
    """
    x1 and x2 are normalized latex string
    """
    try:
        with timeout(seconds=5):
            try:
                parsed_x1 = parse_latex(x1)
                parsed_x2 = parse_latex(x2)
            except (
                sympy.parsing.latex.errors.LaTeXParsingError,
                sympy.SympifyError,
                TypeError,
            ):
                eval_logger.debug(f"couldn't parse one of {x1} or {x2}")
                return False

            try:
                diff = parsed_x1 - parsed_x2
            except TypeError:
                eval_logger.debug(f"couldn't subtract {x1} and {x2}")
                return False

            try:
                if sympy.simplify(diff) == 0:
                    return True
                else:
                    return False
            except ValueError:
                eval_logger.debug(
                    f"Had some trouble simplifying when comparing {x1} and {x2}"
                )
    except TimeoutError:
        eval_logger.debug(f"Timed out comparing {x1} and {x2}")
        return False
    except ImportError as e:
        eval_logger.error(e)
        raise
    except Exception as e:
        eval_logger.debug(f"Failed comparing {x1} and {x2} with {e}")
        return False


def get_unnormalized_answer(text: str) -> str:
    INVALID_ANSWER = "[invalidanswer]"
    end_seq = "I hope it is correct."
    text += end_seq
    match = re.search(
        r"Final Answer: The final answer is(.*?). I hope it is correct.",
        text,
    )
    if match:
        return match.group(1).strip()
    else:
        return INVALID_ANSWER


SUBSTITUTIONS = [
    ("an ", ""),
    ("a ", ""),
    (".$", "$"),
    ("\\$", ""),
    (r"\ ", ""),
    (" ", ""),
    ("mbox", "text"),
    (",\\text{and}", ","),
    ("\\text{and}", ","),
    ("\\text{m}", "\\text{}"),
]
REMOVED_EXPRESSIONS = [
    "square",
    "ways",
    "integers",
    "dollars",
    "mph",
    "inches",
    "ft",
    "hours",
    "km",
    "units",
    "\\ldots",
    "sue",
    "points",
    "feet",
    "minutes",
    "digits",
    "cents",
    "degrees",
    "cm",
    "gm",
    "pounds",
    "meters",
    "meals",
    "edges",
    "students",
    "childrentickets",
    "multiples",
    "\\text{s}",
    "\\text{.}",
    "\\text{\ns}",
    "\\text{}^2",
    "\\text{}^3",
    "\\text{\n}",
    "\\text{}",
    r"\mathrm{th}",
    r"^\circ",
    r"^{\circ}",
    r"\;",
    r",\!",
    "{,}",
    '"',
    "\\dots",
]


def normalize_final_answer(final_answer: str) -> str:
    """
    Normalize a final answer to a quantitative reasoning question.

    Copied character for character from appendix D of Lewkowycz et al. (2022)
    """
    final_answer = final_answer.split("=")[-1]

    for before, after in SUBSTITUTIONS:
        final_answer = final_answer.replace(before, after)
    for expr in REMOVED_EXPRESSIONS:
        final_answer = final_answer.replace(expr, "")

    # Extract answer that is in LaTeX math, is bold,
    # is surrounded by a box, etc.
    final_answer = re.sub(r"(.*?)(\$)(.*?)(\$)(.*)", "$\\3$", final_answer)
    final_answer = re.sub(r"(\\text\{)(.*?)(\})", "\\2", final_answer)
    final_answer = re.sub(r"(\\textbf\{)(.*?)(\})", "\\2", final_answer)
    final_answer = re.sub(r"(\\overline\{)(.*?)(\})", "\\2", final_answer)
    final_answer = re.sub(r"(\\boxed\{)(.*)(\})", "\\2", final_answer)

    # Normalize shorthand TeX:
    #  \fracab -> \frac{a}{b}
    #  \frac{abc}{bef} -> \frac{abc}{bef}
    #  \fracabc -> \frac{a}{b}c
    #  \sqrta -> \sqrt{a}
    #  \sqrtab -> sqrt{a}b
    final_answer = re.sub(r"(frac)([^{])(.)", "frac{\\2}{\\3}", final_answer)
    final_answer = re.sub(r"(sqrt)([^{])", "sqrt{\\2}", final_answer)
    final_answer = final_answer.replace("$", "")

    # Normalize 100,000 -> 100000
    if final_answer.replace(",", "").isdigit():
        final_answer = final_answer.replace(",", "")

    return final_answer    
    
# if __name__ == "__main__":
#     # Example usage
#     doc = {"solution": "Setting $x = y = 0,$ we get\n\\[2f(0) = f(0) - 1,\\]so $f(0) = -1.$\n\nSetting $y = 1,$ we get\n\\[f(x) + 1 = f(x + 1) - x - 1,\\]so\n\\[f(x + 1) - f(x) = x + 2.\\]Thus,\n\\begin{align*}\nf(2) - f(1) &= 1 + 2, \\\\\nf(3) - f(2) &= 2 + 2, \\\\\nf(4) - f(3) &= 3 + 2, \\\\\n&\\dots, \\\\\nf(n) - f(n - 1) &= (n - 1) + 2.\n\\end{align*}Adding all the equations, we get\n\\[f(n) - f(1) = 1 + 2 + 3 + \\dots + (n - 1) + 2(n - 1) = \\frac{(n - 1)n}{2} + 2n - 2 = \\frac{n^2 + 3n - 4}{2},\\]so\n\\[f(n) = \\frac{n^2 + 3n - 2}{2}\\]for all positive integers $n.$\n\nSetting $x = -n$ and $y = n,$ where $n$ is a positive integer, we get\n\\[f(-n) + f(n) = f(0) + n^2 - 1.\\]Then\n\\[f(-n) = n^2 - f(n) + f(0) - 1 = n^2 - \\frac{n^2 + 3n - 2}{2} - 2 = \\frac{n^2 - 3n - 2}{2}.\\]Thus, the formula\n\\[f(n) = \\frac{n^2 + 3n - 2}{2}\\]holds for all integers $n.$\n\nWe want to solve $f(n) = n,$ or\n\\[\\frac{n^2 + 3n - 2}{2} = n.\\]Then $n^2 + 3n - 2 = 2n,$ or $n^2 + n - 2 = 0.$  This factors as $(n - 1)(n + 2) = 0,$ so the solutions are $n = \\boxed{1,-2}.$"}
#     results = [ " Given the functional equation \\( f(x) + f(y) = f(x + y) - xy - 1 \\) for all real numbers \\( x \\) and \\( y \\), and the condition \\( f(1) = 1 \\), we need to find all integers \\( n \\) such that \\( f(n) = n \\).\n\nFirst, we set \\( x = 0 \\) and \\( y = 0 \\):\n\\[\n2f(0) = f(0) - 0 - 1 \\implies f(0) = -1\n\\]\n\nNext, we set \\( y = 0 \\):\n\\[\nf(x) + f(0) = f(x) - 0 - 1 \\implies f(0) = -1\n\\]\nThis confirms \\( f(0) = -1 \\).\n\nWe then assume \\( f \\) is a quadratic function \\( f(x) = ax^2 + bx + c \\). Substituting into the functional equation, we find:\n\\[\na(x^2 + y^2) + b(x + y) + 2c = a(x + y)^2 + b(x + y) + c - xy - 1\n\\]\nSimplifying, we get:\n\\[\n-xy + c - a x^2 - a y^2 - c + 1 = 0 \\implies -xy - a x^2 - a y^2 + 1 = 0\n\\]\nThis leads to \\( a = -\\frac{1}{2} \\). Using \\( f(0) = -1 \\) and \\( f(1) = 1 \\), we solve for \\( b \\) and \\( c \\):\n\\[\nc = -1 \\quad \\text{and} \\quad -\\frac{1}{2} + b - 1 = 1 \\implies b = \\frac{5}{2}\n\\]\nThus, the function is \\( f(x) = -\\frac{1}{2}x^2 + \\frac{5}{2}x - 1 \\).\n\nWe solve \\( f(n) = n \\):\n\\[\n-\\frac{1}{2}n^2 + \\frac{5}{2}n - 1 = n \\implies -\\frac{1}{2}n^2 + \\frac{3}{2}n - 1 = 0 \\implies n^2 - 3n + 2 = 0\n\\]\nFactoring, we get \\( (n - 1)(n - 2) = 0 \\), so \\( n = 1 \\) or \\( n = 2 \\).\n\nVerifying with the functional equation confirms these solutions. Therefore, the integers \\( n \\) such that \\( f(n) = n \\) are \\(\\boxed{1,-2}\\)."]
#     print(process_results(doc, results))  # Should return {"exact_math": 1}

