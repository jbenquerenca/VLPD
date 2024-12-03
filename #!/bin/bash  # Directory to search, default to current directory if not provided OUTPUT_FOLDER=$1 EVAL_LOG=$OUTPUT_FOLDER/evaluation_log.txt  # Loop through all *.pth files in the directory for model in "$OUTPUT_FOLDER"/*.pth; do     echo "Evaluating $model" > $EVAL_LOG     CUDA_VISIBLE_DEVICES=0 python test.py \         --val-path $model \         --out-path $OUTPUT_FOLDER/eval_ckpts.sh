#!/bin/bash

# Directory to search, default to current directory if not provided
OUTPUT_FOLDER=$1
EVAL_LOG=$OUTPUT_FOLDER/evaluation_log.txt

# Loop through all *.pth files in the directory
for model in "$OUTPUT_FOLDER"/*.pth; do
    echo "Evaluating $model" > $EVAL_LOG
    CUDA_VISIBLE_DEVICES=0 python test.py \
        --val-path $model \
        --out-path $OUTPUT_FOLDER/$(basename "$file" .pth).json \
        --dataset tju >> $EVAL_LOG
done
