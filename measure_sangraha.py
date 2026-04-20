from datasets import get_dataset_config_names, get_dataset_split_names, load_dataset
import json
import re

DATASET_NAME = "ai4bharat/sangraha"
CONFIG_NAME = "verified"

# Simple whitespace-based word count.
# Good for most Indic-script and Latin-script text in this dataset.
WORD_RE = re.compile(r"\S+")

def count_words(text: str) -> int:
    if not text:
        return 0
    return len(WORD_RE.findall(text))

def main():
    splits = get_dataset_split_names(DATASET_NAME, CONFIG_NAME)

    results = {}
    total_pdf_rows = 0
    total_words = 0

    for split in splits:
        print(f"Processing split: {split}")

        ds = load_dataset(
            DATASET_NAME,
            CONFIG_NAME,
            split=split,
            streaming=True,
            cache_dir="/projects/data/llmteam/safi/cache"
        )

        pdf_rows = 0
        word_count = 0

        for ex in ds:
            if ex.get("type") == "pdf":
                pdf_rows += 1
                word_count += count_words(ex.get("text", ""))

        results[split] = {
            "pdf_rows": pdf_rows,
            "word_count": word_count,
        }

        total_pdf_rows += pdf_rows
        total_words += word_count

        print(f"  pdf_rows={pdf_rows:,}  word_count={word_count:,}")

    results["_total"] = {
        "pdf_rows": total_pdf_rows,
        "word_count": total_words,
    }

    with open("sangraha_verified_pdf_word_counts.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\nDone.")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
