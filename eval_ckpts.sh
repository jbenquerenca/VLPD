#!/bin/bash
OUTPUT_FOLDER=$1
for file_path in $OUTPUT_FOLDER/*.pth; do
    model_name=$(basename "$file_path" .pth)
    CUDA_VISIBLE_DEVICES=0 python test.py \
        --val-path $OUTPUT_FOLDER/$model_name.pth \
        --out-path $OUTPUT_FOLDER/$model_name \
        --results_file $OUTPUT_FOLDER/$model_name.json \
        --dataset tju
done
