"""Per-(direction, language) filters for the combined IndicGenBench_flores_in dataset.

The repo `google/IndicGenBench_flores_in` exposes a single combined dataset
(no per-pair configs). Each row has a `lang` (ISO code) and a
`translation_direction` ("enxx" or "xxen"). Each task YAML uses
`process_docs: !function utils.filter_<direction>_<code>` to scope its eval
set to one language pair and one direction.
"""

_LANG_CODES = (
    "as", "bn", "brx", "gom", "gu", "hi", "kn", "mai", "ml",
    "mni", "mr", "ne", "or", "pa", "sa", "sat", "ta", "te", "ur",
)
_DIRECTIONS = ("enxx", "xxen")


def _make_filter(direction, code):
    def _fn(dataset):
        return dataset.filter(
            lambda x: x["lang"] == code and x["translation_direction"] == direction
        )
    _fn.__name__ = f"filter_{direction}_{code}"
    _fn.__qualname__ = _fn.__name__
    _fn.__doc__ = f"Keep only rows where lang=={code!r} and translation_direction=={direction!r}."
    return _fn


for _direction in _DIRECTIONS:
    for _code in _LANG_CODES:
        _fn = _make_filter(_direction, _code)
        globals()[_fn.__name__] = _fn
