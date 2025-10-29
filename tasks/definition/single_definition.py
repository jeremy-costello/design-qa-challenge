from utils.call_vlm import get_model_prediction
from utils.image_utils import resize_image
from utils.prompt_builder import build_prompt


SYSTEM_PROMPT = (
    "You are a mechanical engineering expert who can identify parts of a student-designed Formula 1 car "
    "from six views of a 3D CAD model. The component(s) you must name is/are highlighted in pink. "
    "You will be shown six views of the 3D CAD model:"
    "Top-left of the image will be the top view, "
    "Top-middle of the image will be the front view, "
    "Top-right of the image will be an isometric view, "
    "Bottom-left of the image will be the bottom view, "
    "Bottom-middle of the image will be the back view, "
    "Bottom-right of the image will be the left view. "
    "Make sure to only answer with the name of the highlighted component(s) and nothing else."
)


def get_prediction_for_question(
        question: str,
        image_name: str,
        image_dir: str = "./vendor/design_qa/dataset/rule_comprehension/rule_definition_qa",
        max_new_tokens: int = 128
) -> str:
    """
    Generate a model prediction for a question using an associated image.

    Args:
        question (str): The input question or instruction for the model.
        image_name (str): The filename of the image located in the
            specified directory.
        image_dir (str, optional): The directory containing image files.
            Defaults to "./vendor/design_qa/dataset/rule_comprehension/rule_definition_qa".
        max_new_tokens (int, optional): The maximum number of tokens the model
            can generate in its response. Defaults to 128.

    Returns:
        str: The generated text output from the model based on the question and
        image.
    """
    image_path = f"{image_dir}/{image_name}"

    image = resize_image(image_path)

    prompt = build_prompt(
        system_prompt=SYSTEM_PROMPT,
        question=question
    )

    output_text = get_model_prediction(
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        image=image
    )

    return output_text
