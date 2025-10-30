from utils.rule_search import create_rule_texts_map


def get_prediction_for_question(
        question: str
) -> str:
    """
    Retrieve and combine rule-related text for a given question.

    Args:
        question (str): The input question potentially containing rule
            references.

    Returns:
        str: A single combined string of all matched rule texts, or "blank"
        if no relevant rules or text are found.
    """
    rule_map = create_rule_texts_map(question, recurse=False)
    if not rule_map:
        return "blank"

    combined_text = " ".join(chunk for chunks in rule_map.values() for chunk in chunks)
    return combined_text or "blank"
