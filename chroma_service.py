import os
from chromadb import Client
from chromadb.config import Settings

from .embed_service import get_embedding, split_text

# ─── ChromaDB Setup ─────────────────────────────────────────────────────────
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "backend/app/vector_db")
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

client = Client(Settings(persist_directory=CHROMA_DB_DIR))
collection = client.get_or_create_collection("documents")

def ingest_document(doc_id: str, text: str, max_tokens: int = 300):
    """
    Splits `text` into chunks, computes embeddings for each chunk,
    and stores them in ChromaDB. Extensive debug prints included.
    """
    # 1) Split text into chunks
    chunks = split_text(text, max_tokens=max_tokens)
    print(f"[DEBUG][ingest_document] Generated {len(chunks)} chunks for '{doc_id}'")

    if not chunks:
        print(f"[WARN][ingest_document] No chunks generated for '{doc_id}'.")
        return

    ids = []
    embeddings = []
    metadatas = []

    # 2) Loop over each chunk and generate embedding
    for idx, chunk in enumerate(chunks):
        print(f"[DEBUG][ingest_document] Computing embedding for chunk {idx} of '{doc_id}' …")
        try:
            emb = get_embedding(chunk)
        except Exception as e:
            print(f"[ERROR][ingest_document] Embedding failed for chunk {idx} of '{doc_id}': {e}")
            continue

        if emb is None:
            print(f"[WARN][ingest_document] get_embedding returned None for chunk {idx} of '{doc_id}'. Skipping.")
            continue

        print(f"[DEBUG][ingest_document] Embedding complete for chunk {idx} (length {len(emb)})")
        chunk_uid = f"{doc_id}__{idx}"
        ids.append(chunk_uid)
        embeddings.append(emb)
        metadatas.append({
            "doc_id": doc_id,
            "chunk_id": idx,
            "text": chunk
        })

    # 3) Add everything at once to ChromaDB (if any embeddings succeeded)
    if not ids:
        print(f"[WARN][ingest_document] No valid embeddings to persist for '{doc_id}'")
        return

    print(f"[INFO][ingest_document] Adding {len(ids)} embeddings to ChromaDB for '{doc_id}' …")
    try:
        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
        client.persist()
        print(f"[INFO][ingest_document] Persisted {len(ids)} chunks to ChromaDB for '{doc_id}'")
        
    except Exception as e:
        print(f"[ERROR][ingest_document] Failed to add/persist to ChromaDB for '{doc_id}': {e}")
       
