# design-qa-challenge

## Running the code
Running this requires a GPU with sufficient VRAM for running [Qwen3-VL-4B-Instruct-unsloth-bnb-4bit](https://huggingface.co/unsloth/Qwen3-VL-4B-Instruct-unsloth-bnb-4bit).

### Docker
Requires [docker](https://docs.docker.com/engine/install/) and [nvidia container toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

Run ```docker compose up --build```
- This may take a while

### Manually
Requires [git](https://github.com/git-guides/install-git) and [uv](https://docs.astral.sh/uv/getting-started/installation/).

Run the following commands:
- ```
  git clone --depth 1 --single-branch \
  https://github.com/anniedoris/design_qa.git \
  ./vendor/design_qa
  ```
- ```uv python install 3.13```
- ```uv venv --python 3.13```
- ```uv sync --locked```

If you're on Linux:
- ```chmod +x evaluate.sh```
- ```./evaluate.sh```

If you're on Windows:
- ```python -m data.chunk_by_rule```
- ```python -m tasks.retrieval.full_retrieval```
- ```python -m tasks.compilation.full_compilation```
- ```python -m tasks.definition.full_definition```
- ```python -m tasks.presence.full_presence```
- ```python -m tasks.dimension.full_dimension```
- ```python -m tasks.func_perf.full_func_perf```
- ```
  python ./vendor/design_qa/eval/full_evaluation.py \
    --path_to_retrieval ./data/outputs/retrieval_predictions.csv \
    --path_to_compilation ./data/outputs/compilation_predictions.csv \
    --path_to_definition ./data/outputs/definition_predictions.csv \
    --path_to_presence ./data/outputs/presence_predictions.csv \
    --path_to_dimension ./data/outputs/dimension_predictions.csv \
    --path_to_functional_performance ./data/outputs/func_perf_predictions.csv \
    --save_path ./data/outputs/results.txt
  ```
