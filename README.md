# design-qa-challenge
Challenging the [Design QA Benchmark](https://github.com/anniedoris/design_qa).

---

## My Results
My results are in the ```my_outputs``` folder.

I used Qwen3-VL-8B-Instruct quantized to 4 bits, along with some custom agent scaffolding. \
Images are downsized so the smaller side is 896 pixels (while preserving aspect ratio).

### Overall Score
My overall score is 0.735, beating the overall score of all baseline approaches.

### Detailed Scores

| Approach | Retrieval | Compilation | Definition | Presence | Dimension | Functional Performance | Overall |
|-------|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| Naive | 0.082 | 0.137 | 0.358 | 0.500 | 0.500 | 0.500 | 0.346 |
| GPT-4-AllRules | 0.750 | 0.298 | 0.470 | 0.629 | 0.533 | 0.563 | 0.541 |
| GPT-4-RAG | 0.181 | 0.362 | 0.420 | 0.532 | 0.300 | 0.563 | 0.393 |
| LLaVA-1.5-RAG | 0.112 | 0.281 | 0.393 | 0.484 | 0.408 | 0.536 | 0.369 |
| Gemini-1.0-RAG | 0.000 | 0.283 | 0.488 | 0.548 | 0.525 | 0.438 | 0.456 |
| Claude-Opus-RAG | 0.173 | 0.288 | 0.423 | 0.500 | 0.508 | 0.875 | 0.461 |
| GPT-4o-AllRules | 0.881 | 0.424 | 0.540 | **0.726** | **0.825** | **0.938** | 0.722 |
| GPT-4o-RAG | 0.185 | 0.376 | 0.525 | 0.710 | 0.675 | 0.750 | 0.537 |
| **Qwen3-VL-8B-Agent (Mine)** | **0.970** | **0.660** | **0.572** | 0.677 | 0.717 | 0.813 | **0.735** |

---

## Running the Code
Running this requires a GPU with sufficient VRAM for running [Qwen3-VL-8B-Instruct-unsloth-bnb-4bit](https://huggingface.co/unsloth/Qwen3-VL-8B-Instruct-unsloth-bnb-4bit).

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
  - This may take a while at the start since it has to download the VLM from Hugging Face.
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

---

## Tunable Parameters
System prompts:
- ```tasks/definition/single_definition.py```
- ```tasks/presence/single_presence.py```
- ```tasks/dimension/single_dimension.py```
- ```tasks/func_perf/single_func_perf.py```
- ```utils/mech_parts.py```

Generation parameters:
- ```utils/call_vlm.py```
  - ```MODEL_NAME``` (which Qwen3 model to use)
    - could also change ```model = *.from_pretrained```, haven't tested it though
  - ```temperature``` (explained [here](https://www.ibm.com/think/topics/llm-temperature))
  - ```top_p``` (explained in temperature link)
  - ```top_k``` (explained in temperature link)

Image parameters:
- ```utils/image_utils.py```
  - ```min_size``` (number of pixels to downscale the smaller side of the image to, while preserving the aspect ratio)
