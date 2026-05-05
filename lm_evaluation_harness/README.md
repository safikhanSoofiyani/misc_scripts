# LM Evaluation Harness — Indic Eval Scripts

Wrapper scripts and custom task configs for running [EleutherAI `lm-evaluation-harness`](https://github.com/EleutherAI/lm-evaluation-harness) over Indic languages on a vLLM backend.

The same set of tasks is wired up for three model regimes (pre-train, post-train, post-train with thinking). Pick the script that matches the model you're evaluating.

## Layout

```
lm_evaluation_harness/
├── README.md
├── requirements.txt
├── run_pre_train.sh             # base / pre-trained models (few-shot, no chat template)
├── run_post_train.sh            # instruct / post-trained models (0-shot, chat template, thinking off)
├── run_post_train_think.sh      # instruct models with reasoning enabled (0-shot, chat template, thinking on)
└── custom_configs/
    ├── pre_train/               # task YAMLs used by run_pre_train.sh
    ├── post_train/              # task YAMLs used by run_post_train.sh
    └── post_train_think/        # task YAMLs used by run_post_train_think.sh
```

## Installation

```bash
# 1. Create environment
conda create -n lmeval python=3.11 -y
conda activate lmeval

# 2. Clone the fork (custom Indic tasks live here)
git clone https://github.com/safikhanSoofiyani/lm-evaluation-harness.git
cd lm-evaluation-harness

# 3. Install
pip install -e .
pip install -e ".[vllm]"

# 4. Extra runtime deps for the custom tasks
pip install -r /path/to/this/repo/lm_evaluation_harness/requirements.txt
```

Set your Hugging Face token in the chosen run script (`HF_TOKEN=""`) or pre-authenticate with `hf auth login` and remove the login line.

## Usage

From this directory:

```bash
bash run_post_train.sh \
  --model_id <hf_id_or_local_path> \
  --lang_bucket <low_res|high_res|all> \
  --task_bucket <bucket(s)> \
  --run_name <output_subdir> \
  --tp_size <tensor_parallel_size> \
  --limit <num_examples_per_task>
```

Swap `run_post_train.sh` for `run_pre_train.sh` or `run_post_train_think.sh` depending on the model.

### Arguments

| Argument        | Required | Description                                                                                              |
| --------------- | :------: | -------------------------------------------------------------------------------------------------------- |
| `--model_id`    | yes      | Hugging Face model ID (e.g., `meta-llama/Llama-3.1-8B-Instruct`) or local model path                     |
| `--lang_bucket` | no       | `low_res`, `high_res`, or `all` (default: `all`). `milu` and `translation` apply their own language sets |
| `--task_bucket` | no       | Comma-separated buckets: `academic`, `reasoning`, `reading`, `math`, `code`, `translation`, or `all`     |
| `--run_name`    | no       | Subdirectory under `outputs/` for results                                                                |
| `--tp_size`     | no       | vLLM tensor parallel size (default: 4)                                                                   |
| `--limit`       | no       | Cap examples per task (useful for smoke tests)                                                           |

### Task buckets

| Bucket        | Tasks                                                                                                |
| ------------- | ---------------------------------------------------------------------------------------------------- |
| `academic`    | `mmlu`, `mmlu_pro`, `milu`                                                                           |
| `reasoning`   | `ai2_arc` (easy + challenge), `boolq`, `trivia_qa`, `commonsense_qa`, `piqa`, `siqa`, `openbookqa`, `winogrande` |
| `reading`     | `race/race_high`, `race/race_middle` (+ `squad_v2` for `pre_train`)                                  |
| `math`        | `gsm8k`, `math500`, `drop`, `gpqa` (main + diamond + extended)                                       |
| `code`        | `humaneval`, `mbpp`                                                                                  |
| `translation` | `indic_gen_bench_flores_in_en_xx`, `indic_gen_bench_flores_in_xx_en`                                 |

### Language buckets

- `high_res`: assamese, bengali, english, gujarati, hindi, kannada, malayalam, marathi, nepali, odiya, punjabi, sanskrit, tamil, telugu, urdu
- `low_res`: bodo, dogri, kashmiri, konkani, maithili, manipuri, santali, sindhi
- Tasks tile per language as `<task_name>_<lang>` (e.g., `mmlu_hindi`)
- `milu` is restricted to the languages it ships (english, bengali, gujarati, hindi, kannada, malayalam, marathi, odiya, punjabi, tamil, telugu)
- `translation` runs on its own fixed list (high_res minus english, plus bodo, konkani, maithili, manipuri, santali)

## Differences between the three scripts

|                       | `run_pre_train.sh` | `run_post_train.sh` | `run_post_train_think.sh` |
| --------------------- | ------------------ | ------------------- | ------------------------- |
| Configs               | `custom_configs/pre_train` | `custom_configs/post_train` | `custom_configs/post_train_think` |
| `num_fewshot`         | 5 (3 for `mbpp`)   | 0                   | 0                         |
| `apply_chat_template` | no                 | yes                 | yes                       |
| `enable_thinking`     | n/a                | `False`             | `True`                    |
| `max_model_len`       | 8192               | 16385               | 16385                     |
| `max_gen_toks`        | 4096               | 8192                | 8192                      |
| `gpu_memory_utilization` | 0.7             | 0.8                 | 0.8                       |

All three use `temperature=0.1`, `seed=42`, `batch_size=auto`, and the vLLM backend.

## Output

Results land under `outputs/<run_name>/`, with per-task JSON summaries plus per-sample logs (`--log_samples`).

## Notes

- `HF_HOME` is set inside each script — point it at a cache that has enough room for the model + datasets before running.
- Code-eval tasks (`humaneval`, `mbpp`) run with `HF_ALLOW_CODE_EVAL=1` and `--confirm_run_unsafe_code`; only run on trusted infra.
- Edit `INCLUDE_PATH` in the script if you keep custom configs elsewhere.
