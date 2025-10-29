from utils.call_vlm import get_model_prediction
from utils.prompt_builder import build_prompt


SYSTEM_PROMPT = (
    "You are a technical expert in mechanical and automotive engineering, specializing in interpreting FSAE rule-related queries. "
    "You will be given a text string (a question) and must identify key technical terms of interest that could be used to find relevant FSAE rules. "
    "After identifying the main terms, you must also generate additional related terms or synonyms that could appear in rule text, "
    "to help improve exact text matching. "
    "Output all terms as a comma-separated list (lowercase), without explanations or extra words. "
    "For example, for the text:\n\n"
    "'We are a student engineering team designing a vehicle for the FSAE competition. "
    "Attached is the FSAE rules document. Please list all rules relevant to `Aerodynamic/Aerodynamics`. "
    "Answer with only the rule numbers (i.e.: AA.1.1.1) separated by commas and no other words.\n\n"
    "The rules relevant to `Aerodynamic/Aerodynamics` are:'\n\n"
    "You should output something like:\n"
    "`aerodynamic, aerodynamics, aero, aero device, downforce, drag, wing, airfoil`\n\n"
    "Ignore where the question says to answer with only the rule numbers. Answer with the list of terms."
)


def extract_terms_of_interest(
        question: str,
        max_new_tokens: int = 256
) -> list[str]:
    """
    Extract and expand terms of interest from a question for rule matching.

    Args:
        question (str): The input question or text from which to extract key terms.
        max_new_tokens (int, optional): Maximum tokens to generate in model response.
            Defaults to 128.

    Returns:
        list[str]: A list of lowercase terms and variants for text matching.
    """
    prompt = build_prompt(
        system_prompt=SYSTEM_PROMPT,
        question=question
    )

    output_text = get_model_prediction(
        prompt=prompt,
        max_new_tokens=max_new_tokens,
    )

    # Parse comma-separated list
    terms = [t.strip().lower() for t in output_text.split(",") if t.strip()]
    terms = list(set(terms))
    return terms
