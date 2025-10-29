from utils.call_vlm import get_model_prediction
from utils.image_utils import resize_image
from utils.prompt_builder import build_prompt
from utils.mech_parts import create_mech_texts_map


SYSTEM_PROMPT = (
    "You are a mechanical engineering expert who can identify whether a specific part of a student-designed Formula 1 car "
    "is present in an image containing a close-up of a 3D CAD model with six views of the same 3D CAD model below the close-up. "
    "You will be shown seven views of the 3D CAD model and must respond yes or no as to whether the specific part is present. "
    "At the top of the image is a close-up of the area for which you must identify if the specific part is present. "
    "Below this close-up are six views of the same 3D CAD model (fully zoomed out). "
    "Top-left of the zoomed-out views will be the top view, "
    "Top-middle of the zoomed-out views will be the front view, "
    "Top-right of the zoomed-out views will be an isometric view, "
    "Bottom-left of the zoomed-out views will be the bottom view, "
    "Bottom-middle of the zoomed-out views will be the back view, "
    "Bottom-right of the zoomed-out views will be the left view. "
    "Make sure to only answer with yes or no, depending on whether the specific part is present."
)


def get_prediction_for_question(
        question: str,
        image_name: str,
        image_dir: str = "./vendor/design_qa/dataset/rule_comprehension/rule_presence_qa",
        max_new_tokens: int = 1
) -> str:
    """
    Generate a deterministic model prediction for a question using an image
    and related mechanical text context.

    Args:
        question (str): The input question to query the model.
        image_name (str): The filename of the image associated with the question.
        image_dir (str, optional): The directory containing image files.
            Defaults to "./vendor/design_qa/dataset/rule_comprehension/rule_presence_qa".
        max_new_tokens (int, optional): The maximum number of tokens to generate.
            Defaults to 1 (suitable for short answers like "yes" or "no").

    Returns:
        str: The model's generated prediction text.
    """
    image_path = f"{image_dir}/{image_name}"

    image = resize_image(image_path)

    mech_texts_map = create_mech_texts_map(question)

    prompt = build_prompt(
        system_prompt=SYSTEM_PROMPT,
        question=question,
        mech_texts_map=mech_texts_map
    )

    output_text = get_model_prediction(
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        image=image,
        deterministic=True
    )

    return output_text
