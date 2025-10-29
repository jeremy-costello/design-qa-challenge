from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
import torch
from PIL import Image


MODEL_NAME = "unsloth/Qwen3-VL-4B-Instruct-unsloth-bnb-4bit"
MODEL_DIR = "./models"


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = Qwen3VLForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    dtype="auto",
    device_map="auto",
    cache_dir=MODEL_DIR
).to(device)
processor = AutoProcessor.from_pretrained(
    MODEL_NAME,
    cache_dir=MODEL_DIR
)


def get_model_prediction(
        prompt: str,
        max_new_tokens: int,
        image: Image.Image | None = None,
        deterministic: bool = False,
):
    """
    Generate a model prediction from a text prompt (optionally with an image).

    Args:
        prompt (str): The input text prompt to guide generation.
        max_new_tokens (int): The maximum number of new tokens to generate.
        deterministic (bool, optional): If True, generation is deterministic
            (no sampling, single-beam search). If False, generation may include
            sampling or beam search depending on model settings.
            Defaults to False.
        image (Image | None, optional): An optional image to include in the
            input, used for multimodal models. Defaults to None.

    Returns:
        str: The generated text output from the model, stripped of any leading
        or trailing whitespace.
    """
    content = []
    if image is not None:
        content.append({
            "type": "image",
            "image": image
        })
    content.append({
        "type": "text",
        "text": prompt
    })

    messages = [
        {
            "role": "user",
            "content": content,
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        if deterministic:
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                num_beams=1,
                temperature=None,
                top_p=None,
                top_k=None
            )
        else:
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens
            )

    # trims input tokens
    trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, generated_ids)]

    output_text = processor.batch_decode(
        trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )[0].strip()

    return output_text
