from utils.call_vlm import get_model_prediction
from utils.image_utils import resize_image
from utils.prompt_builder import build_prompt
from utils.rule_search import create_rule_texts_map
from utils.mech_parts import create_mech_texts_map


SYSTEM_PROMPT = (
    "You are a mechanical engineering expert specializing in Formula SAE (FSAE) design compliance, "
    "materials, and FEA (finite element analysis) evaluation. "
    "You will be shown an image displaying FEA simulation results for a vehicle component. "
    "Your goal is to determine whether the design complies with the specified FSAE rule(s) "
    "based on the visual stress/strain results, material information, and rule text. "
    "Use the rule text(s) and any provided contextual mechanical information to reason about compliance. "
    "Follow the exact answer structure requested in the question: "
    "start your explanation with 'Explanation:' and your final yes/no summary with 'Answer:'."
)


def get_prediction_for_question(
        question: str,
        image_name: str,
        image_dir: str = "./vendor/design_qa/dataset/rule_compliance/rule_functional_performance_qa/images",
        max_new_tokens: int = 512
) -> str:
    image_path = f"{image_dir}/{image_name}"

    image = resize_image(image_path)

    rule_texts_map = create_rule_texts_map(
        question=question,
        recurse=True
    )

    mech_texts_map = create_mech_texts_map(question)

    prompt = build_prompt(
        system_prompt=SYSTEM_PROMPT,
        question=question,
        rule_texts_map=rule_texts_map,
        mech_texts_map=mech_texts_map
    )

    output_text = get_model_prediction(
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        image=image
    )

    return output_text
