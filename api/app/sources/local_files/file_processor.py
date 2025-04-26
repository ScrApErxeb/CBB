from typing import List

def clean_text(text: str) -> str:
    return text.strip().replace("\n\n", "\n")

def split_text(text: str, chunk_size: int = 500) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def process_text(text: str) -> List[str]:
    cleaned = clean_text(text)
    return split_text(cleaned)
