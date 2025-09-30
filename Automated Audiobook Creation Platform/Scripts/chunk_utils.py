def simple_chunker(text, max_chars=4000, overlap=200):
    """
    Chunk text into pieces < max_chars with a small overlap (chars).
    """
    text = text.strip()
    n = len(text)
    start = 0
    chunks = []
    while start < n:
        end = min(start + max_chars, n)
        if end < n:
            cut = text.rfind("\n", start, end)
            if cut <= start:
                cut = text.rfind(" ", start, end)
            if cut <= start:
                cut = end
            end = cut
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = max(end - overlap, end)
    return chunks
