from pathlib import Path
import re


INPUT_FILE = "./vendor/design_qa/dataset/docs/rules_pdfplumber1.txt"
OUTPUT_DIR = "./data/chunks"

RULE_REGEX = re.compile(r"^([A-Z]+(?:\.\d+)+)")
DOTS_REGEX = re.compile(r"\.{5,}")


def chunk_text_by_rule(
        file_path: str
) -> list[str]:
    """
    Split a text file into chunks based on a rule regex.

    Args:
        file_path: Path to the input text file.

    Returns:
        A list of text chunks.
    """
    lines = [line.rstrip() for line in open(file_path, "r", encoding="utf-8")]
    chunks = []
    current_chunk = []

    for line in lines:
        if RULE_REGEX.match(line) and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
        current_chunk.append(line)

    if current_chunk:
        chunks.append(current_chunk)

    chunk_texts = ["\n".join(chunk) for chunk in chunks]
    filtered_chunks = [chunk for chunk in chunk_texts if not DOTS_REGEX.search(chunk)]
    return filtered_chunks


def save_chunks(
        chunks: list[str],
        output_dir: str
) -> None:
    """
    Save a list of text chunks to individual files.

    Args:
        chunks: List of text chunks to save.
        output_dir: Directory to save the chunks in.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    for i, chunk in enumerate(chunks, 1):
        file_path = out_path / f"chunk_{i:03}.txt"
        file_path.write_text(chunk, encoding="utf-8")


def main():
    chunks = chunk_text_by_rule(INPUT_FILE)
    save_chunks(chunks, OUTPUT_DIR)


if __name__ == "__main__":
    main()
