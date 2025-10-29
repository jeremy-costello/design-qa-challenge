from pathlib import Path


def search_by_keyword(
        search_term: str,
        chunk_dir: str = "./data/chunks"
) -> list[str]:
    """
    Search for text chunks containing a given keyword within a directory.

    Args:
        search_term (str): The keyword or phrase to search for in text files.
        chunk_dir (str, optional): The directory containing text chunks.
            Defaults to "./data/chunks".

    Returns:
        list[str]: A list of text strings (one per matching file) that contain
        the search term.
    """
    path = Path(chunk_dir)
    matching_chunks = []

    for f in path.glob("*.txt"):
        text = f.read_text(encoding="utf-8")
        if search_term.lower() in text.lower():
            matching_chunks.append(text.strip())

    return matching_chunks
