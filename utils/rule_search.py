import re
from pathlib import Path


# Match things like V.1.2, F.3.5.3, F.3.5.3b, F.3.5.3.b, etc.
RULE_REGEX = re.compile(r"rule\s+([A-Z]+(?:\.\d+)+(?:[a-z])?)", re.IGNORECASE)


def extract_rule_numbers(
        text: str
) -> list[str]:
    """
    Extract all rule numbers from the given text.

    Args:
        text (str): The input text to search.

    Returns:
        list[str]: A list of all rule numbers found in the text.
                   Returns an empty list if no matches are found.
    """
    matches = RULE_REGEX.findall(text)
    normalized = [
        re.sub(r"[a-z]+$|\.+$", "", m) for m in matches
    ]
    return list(dict.fromkeys(normalized))


def find_rule_text(
        rule_number: str,
        chunk_dir: str = "./data/chunks"
) -> list[str]:
    """
    Find and return text chunks corresponding to a specific rule number.

    Args:
        rule_number (str): The rule number to search for
        chunk_dir (str, optional): The directory containing text chunks.
            Defaults to "./data/chunks".

    Returns:
        list[str]: A list of text chunks where the first word matches the
        specified rule number. Each string contains the text following the rule
        number. Returns an empty list if no matches are found.
    """
    path = Path(chunk_dir)
    matching_chunks = []

    for f in path.glob("*.txt"):
        words = f.read_text(encoding="utf-8").strip().split()
        if not words:
            continue

        # Only consider chunks where the first "word" matches the rule number
        if words[0] == rule_number:
            # Remove the rule number and join remaining words
            chunk_text = " ".join(words[1:]).strip()
            matching_chunks.append(chunk_text)

    return matching_chunks


def create_rule_texts_map(
        question: str,
        recurse: bool = False
) -> dict[str, list[str]]:
    """
    Build a mapping of rule numbers to their corresponding text content.

    Args:
        question (str): The input text or query containing one or more rule
            references.

    Returns:
        dict[str, list[str]]: A dictionary where each key is a rule number and
        each value is a list of text chunks associated with that rule.
    """
    rule_numbers = extract_rule_numbers(question)
    rule_texts_map = {}

    for rule in rule_numbers:
        texts = find_rule_text(rule)
        if texts:
            rule_texts_map[rule] = texts

    if recurse:
        for rule, texts in list(rule_texts_map.items()):
            for t in texts:
                referenced = extract_rule_numbers(t)
                for ref in referenced:
                    if ref not in rule_texts_map:
                        ref_texts = find_rule_text(ref)
                        if ref_texts:
                            rule_texts_map[ref] = ref_texts

    return rule_texts_map
