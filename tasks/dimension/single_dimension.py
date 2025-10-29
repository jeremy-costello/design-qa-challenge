from utils.call_vlm import get_model_prediction
from utils.image_utils import resize_image
from utils.prompt_builder import build_prompt
from utils.rule_search import create_rule_texts_map


SYSTEM_PROMPT = (
    "You are a mechanical engineering design compliance expert specializing in Formula SAE (FSAE) rules. "
    "You will be shown an image that contains seven CAD-related views of a Formula SAE vehicle design: "
    "a top section showing an engineering drawing with dimensions, and six smaller CAD views below it, "
    "each corresponding to standard orientations (top, front, isometric, bottom, back, left). "
    "The engineering drawing has the same orientation as one of the CAD views and includes explicit linear or angular dimensions. "
    "All dimensions are in millimeters (mm). "
    "Your task is to determine whether the design shown in the image complies with the specified FSAE rule(s). "
    "Use only the dimensions explicitly visible in the engineering drawing to reason about compliance. "
    "If a relevant dimension is not shown, assume it complies with the rules. "
    "When answering, you must strictly follow the format specified in the question prompt: "
    "first provide a short reasoning statement starting with 'Explanation:', "
    "and then provide a final compliance statement starting with 'Answer:' followed by either 'yes' or 'no'. "
    "Ensure that your answer is clear, concise, and consistent with the requested output structure."
)


def get_prediction_for_question(
        question: str,
        image_name: str,
        image_dir: str = "./vendor/design_qa/dataset/rule_compliance/rule_dimension_qa/context",
        max_new_tokens: int = 512
) -> str:
    """
    Generate a model prediction for a rule compliance question using both
    textual and visual context.

    Args:
        question (str): The input question to query the model, typically
            referencing one or more rule numbers.
        image_name (str): The filename of the image providing visual context.
        image_dir (str, optional): The directory containing image files.
            Defaults to "./vendor/design_qa/dataset/rule_compliance/rule_dimension_qa/context".
        max_new_tokens (int, optional): The maximum number of tokens to generate
            in the model's response. Defaults to 512.

    Returns:
        str: The generated text prediction from the model.
    """
    image_path = f"{image_dir}/{image_name}"

    image = resize_image(image_path)

    rule_texts_map = create_rule_texts_map(
        question=question,
        recurse=True
    )

    prompt = build_prompt(
        system_prompt=SYSTEM_PROMPT,
        question=question,
        rule_texts_map=rule_texts_map
    )

    output_text = get_model_prediction(
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        image=image
    )

    return output_text
