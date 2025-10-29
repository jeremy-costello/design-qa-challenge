#!/bin/bash
source .venv/bin/activate

echo "Chunking rules text."
python -m data.chunk_by_rule

echo "Running retrieval task."
python -m tasks.retrieval.full_retrieval

echo "Running compilation task."
python -m tasks.compilation.full_compilation

echo "Running definition task."
python -m tasks.definition.full_definition

echo "Running presence task."
python -m tasks.presence.full_presence

echo "Running dimension task."
python -m tasks.dimension.full_dimension

echo "Running functional performance task."
python -m tasks.func_perf.full_func_perf

rm ./data/outputs/results.txt

echo "Running Design QA evaluation."
python ./vendor/design_qa/eval/full_evaluation.py \
    --path_to_retrieval ./data/outputs/retrieval_predictions.csv \
    --path_to_compilation ./data/outputs/compilation_predictions.csv \
    --path_to_definition ./data/outputs/definition_predictions.csv \
    --path_to_presence ./data/outputs/presence_predictions.csv \
    --path_to_dimension ./data/outputs/dimension_predictions.csv \
    --path_to_functional_performance ./data/outputs/func_perf_predictions.csv \
    --save_path ./data/outputs/results.txt
