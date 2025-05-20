from sentence_transformers import SentenceTransformer
import tiktoken

# ─── Load a small, fast local model ──────────────────────────────────────────
# "all-MiniLM-L6-v2" is ~85 MB and gives good results for semantic search.
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> list[float]:
    """
    Returns a float vector for `text` using a local SentenceTransformer model.
    """
    # strip newlines so embedding is purely about content
    cleaned = text.replace("\n", " ")
    embedding = model.encode(cleaned, convert_to_numpy=True)
    return embedding.tolist()


def split_text(text: str, max_tokens: int = 300) -> list[str]:
    """
    Splits long `text` into smaller chunks, each under max_tokens tokens,
    using tiktoken for precise token counts.
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    words = text.split()
    chunks, current = [], []

    for w in words:
        current.append(w)
        if len(tokenizer.encode(" ".join(current))) > max_tokens:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))
    return chunks


# ─── Quick test when run directly ────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing local embedder…")
    s = "The tribunal penalized the firm under SEBI Act, Clause 49."
    emb = get_embedding(s)
    print("→ Embedding length:", len(emb))
    print("→ First 5 values:", emb[:5])
