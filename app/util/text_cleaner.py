def chunk_text(text: str, max_tokens: int = 1000) -> list[str]:
    """
    Splits the text into chunks that are within the max token limit.
    Assumes 1 token ≈ 4 characters.
    """
    max_chars = max_tokens * 4  # Convert token limit to character limit
    chunks = []
    current_chunk = []

    for paragraph in text.split("\n"):  # Split by paragraphs
        if sum(len(line) for line in current_chunk) + len(paragraph) + 1 <= max_chars:
            current_chunk.append(paragraph)
        else:
            chunks.append("\n".join(current_chunk))
            current_chunk = [paragraph]

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks