#!/bin/bash

set -e

# ================= ARGUMENT PARSING =================
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --model_id) MODEL_ID="$2"; shift ;;
        --lang_bucket) LANG_BUCKET="$2"; shift ;;  # high, low, or all
        --task_bucket) TASK_BUCKET="$2"; shift ;;  # e.g., reasoning, math, qa, all
        --run_name) RUN_NAME="$2"; shift ;;  # optional, for output directory naming
        --tp_size) TP_SIZE="$2"; shift ;;  # tensor parallel size, default is 4
        --limit) LIMIT="$2"; shift ;;  # optional, limit number of tasks
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# ************** CHANGE THESE VALUES **************
export VLLM_LOGGING_LEVEL=ERROR
export HF_HOME="/projects/data/llmteam/safi/cache"
INCLUDE_PATH="custom_configs/post_train_think"
HF_TOKEN="" # Add your token here if needed

# ================= LANGUAGE GROUPS =================
LOW_RES_LANGS="bodo,dogri,kashmiri,konkani,maithili,manipuri,santali,sindhi"
HIGH_RES_LANGS="assamese,bengali,english,gujarati,hindi,kannada,malayalam,marathi,nepali,odiya,punjabi,sanskrit,tamil,telugu,urdu"

# ================= TASK GROUPS =================
declare -A TASK_GROUPS
TASK_GROUPS["academic"]="mmlu,mmlu_pro,milu"
TASK_GROUPS["reasoning"]="ai2_arc_arc-easy,ai2_arc_arc-challenge,boolq,trivia_qa,commonsense_qa,piqa,siqa,openbookqa,winogrande"
TASK_GROUPS["reading"]="race/race_high,race/race_middle"
TASK_GROUPS["math"]="gsm8k,math500,drop,gpqa/gpqa_main,gpqa/gpqa_diamond,gpqa/gpqa_extended"
TASK_GROUPS["code"]="humaneval,mbpp"
TASK_GROUPS["translation"]="indic_gen_bench_flores_in_en_xx,indic_gen_bench_flores_in_xx_en"


BACKEND="vllm"
TP_SIZE=${TP_SIZE:-4}  # Default tensor parallel size

COMMON_ARGS="pretrained=${MODEL_ID},max_model_len=16385,dtype=auto,gpu_memory_utilization=0.8,tensor_parallel_size=${TP_SIZE},trust_remote_code=True,enable_thinking=True"
COMMON_GEN_KWARGS="temperature=0.1,max_gen_toks=8192"


if [[ -z "$MODEL_ID" ]]; then
    echo "Model ID is required. Use --model_id to specify it."
    exit 1
fi

if [[ -n "$LIMIT" ]]; then
    LIMIT_ARG="--limit $LIMIT"
else
    LIMIT_ARG=""
fi



hf auth login --token $HF_TOKEN



if [[ -z "$TASK_BUCKET" || "$TASK_BUCKET" == "all" ]]; then
    TASK_BUCKETS=(${!TASK_GROUPS[@]})
else
    IFS=',' read -r -a TASK_BUCKETS <<< "$TASK_BUCKET"
fi

echo "Selected Task Buckets: ${TASK_BUCKETS[@]}"

# ================= RUN EVALS PER TASK =================
for BUCKET in "${TASK_BUCKETS[@]}"; do
    IFS=',' read -ra TASK_PATHS <<< "${TASK_GROUPS[$BUCKET]}"
    for TASK_PATH in "${TASK_PATHS[@]}"; do
        IFS='/' read -ra SPLIT <<< "$TASK_PATH"
        TASK_NAME="${SPLIT[-1]}"
        
        echo "---------------------------------------------------------"
        echo "Preparing to run evaluation for task: $TASK_NAME"
        echo "---------------------------------------------------------"
        if [[ "$LANG_BUCKET" == "low_res" ]]; then
            LANG_LIST="$LOW_RES_LANGS"
        elif [[ "$LANG_BUCKET" == "high_res" ]]; then
            LANG_LIST="$HIGH_RES_LANGS"
        else
            LANG_LIST="$HIGH_RES_LANGS,$LOW_RES_LANGS"
        fi

        #if task is milu, then only run a few languages
        if [[ "$TASK_NAME" == "milu" ]]; then
            LANG_LIST="english,bengali,gujarati,hindi,kannada,malayalam,marathi,odiya,punjabi,tamil,telugu"
        fi

        if [[ "$BUCKET" == "translation" ]]; then
            LANG_LIST="assamese,bengali,gujarati,hindi,kannada,malayalam,marathi,nepali,odiya,punjabi,sanskrit,tamil,telugu,urdu,bodo,konkani,maithili,manipuri,santali"
        fi

        CURRENT_EVAL_TASKS=$(echo $LANG_LIST | tr ',' '\n' | sed "s/^/${TASK_NAME}_/" | paste -sd "," -)
        OUTPUT_DIR="outputs/${RUN_NAME}"
        
        # Run lm_eval for the current group of tasks
        HF_ALLOW_CODE_EVAL="1" lm_eval --model "$BACKEND" \
          --model_args "$COMMON_ARGS" \
          --gen_kwargs "$COMMON_GEN_KWARGS" \
          --include_path "$INCLUDE_PATH" \
          --tasks "$CURRENT_EVAL_TASKS" \
          --confirm_run_unsafe_code \
          $LIMIT_ARG \
          --num_fewshot 0 \
          --output_path "$OUTPUT_DIR" \
          --log_samples \
          --seed 42 \
          --apply_chat_template \
          --batch_size auto

    done
done
