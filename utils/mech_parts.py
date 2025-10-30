from utils.call_vlm import get_model_prediction
from utils.prompt_builder import build_prompt
from utils.keyword_search import search_by_keyword


SYSTEM_PROMPT = (
    "You are a mechanical engineering expert who can identify mechanical part names of interest from a text string. "
    "You will be given a text string and must identify mechanical engineering part names from it. "
    "Only respond with the part name of interest, separated by commas. For example, this text string:\n\n"
    "We are a student engineering team designing a vehicle for the FSAE competition. "
    "Attached is the FSAE rules document. Also attached is an image showing seven CAD views (each boxed in black) of our vehicle design. "
    "The top, big view shows a close-up view of the design. "
    "The six smaller views on the bottom of the image show different complete views of the CAD of the vehicle and are provided for context. "
    "Note that the close-up view orientation matches one of the six complete view orientations. "
    "The close-up view may also have some components hidden (with respect to the corresponding complete view) for visualization of specific components. "
    "Looking at the close-up view, is/are any part of the the front hoop or the front roll hoop visible in the close-up view? Answer simply with yes or no. "
    "\n\nShould be responded to with `front hoop, front roll hoop`. Remember to separate part names with a comma."
)


def extract_mechanical_parts(
        question: str,
        max_new_tokens: int = 128
) -> list[str]:
    """
    Extract a list of mechanical parts mentioned in a question using an LLM.

    Args:
        question (str): The input text or question from which to extract
            mechanical part names.
        max_new_tokens (int, optional): The maximum number of tokens to
            generate in the model's response. Defaults to 128.

    Returns:
        list[str]: A list of mechanical part names extracted from the question.
    """
    prompt = build_prompt(
        system_prompt=SYSTEM_PROMPT,
        question=question
    )
    output_text = get_model_prediction(
        prompt=prompt,
        max_new_tokens=max_new_tokens,
    )

    parts = [p.strip() for p in output_text.split(",") if p.strip()]
    parts = list(set(parts))
    return parts


def create_mech_texts_map(
        question: str,
) -> dict[str, list[str]]:
    """
    Build a mapping of mechanical terms to their matching text data.

    Args:
        question (str): The input text or question containing mechanical terms.

    Returns:
        dict[str, list[str]]: A dictionary where each key is a mechanical part
        name, and each value is a list of text strings containing matches for
        that term.
    """
    mech_terms = extract_mechanical_parts(question)
    mech_texts_map = {}

    for term in mech_terms:
        matches = search_by_keyword(term)
        if matches:
            mech_texts_map[term] = matches

    return mech_texts_map
