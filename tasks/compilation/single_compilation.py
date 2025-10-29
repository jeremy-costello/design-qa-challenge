import re
from pathlib import Path
from utils.keyword_search import search_by_keyword


TERMS_REGEX = re.compile(r"`([^`]+)`")


def extract_terms(
        question: str
):
    """
    Extract search terms enclosed in backticks from a question.

    Args:
        question (str): The input text or question containing terms enclosed
            in backticks.

    Returns:
        list[str]: A list of extracted terms. Returns an empty list if no
        backtick-enclosed terms are found.
    """
    match = TERMS_REGEX.search(question)
    if not match:
        return []
    return [t.strip() for t in match.group(1).split("/")]


def find_matching_rules(
        search_terms: list,
        chunk_dir: str = "./data/chunks"
):
    """
    Find rule numbers from text files that contain any of the given search terms.

    Args:
        search_terms (list[str]): A list of keywords or terms to search for.
        chunk_dir (str, optional): Directory path containing text chunks.
            Defaults to "./data/chunks".

    Returns:
        list[str]: A list of unique rule numbers (first words of matching files)
        where at least one search term appears.
    """
    path = Path(chunk_dir)
    rule_numbers = []

    for f in path.glob("*.txt"):
        text = f.read_text(encoding="utf-8")
        if any(term in text for term in search_terms):
            first_word = text.strip().split()[0]
            rule_numbers.append(first_word)

    return list(set(rule_numbers))


def get_prediction_for_question(
        question: str
) -> str:
    """
    Generate a comma-separated list of rule numbers matching terms in a question.

    Args:
        question (str): The input question or query containing backtick-enclosed
            search terms.

    Returns:
        str: A comma-separated string of rule numbers matching the extracted
        terms, or "blank" if no matches are found.
    """
    search_terms = extract_terms(question)
    if not search_terms:
        return "blank"

    rule_list = find_matching_rules(search_terms)
    rules_string = ", ".join(rule_list)
    return rules_string
