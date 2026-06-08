"""Milestone 4 — Embed chunks into ChromaDB and retrieve.

Pipeline stage (per planning.md):
  chunks.json -> Embedding (all-MiniLM-L6-v2, sentence-transformers, local)
              -> Vector store (ChromaDB, persistent, local)
              -> Retrieval (semantic search, top-k, ChromaDB .query())

Usage:
  .venv\\Scripts\\python.exe embed_store.py     # (re)build the vector store
  from embed_store import retrieve              # use in test_retrieval.py / app
"""
import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent
CHUNKS = ROOT / "data" / "chunks" / "chunks.json"
CHROMA_DIR = ROOT / "data" / "chroma"
COLLECTION = "unofficial_guide"
MODEL_NAME = "all-MiniLM-L6-v2"

# Lazily-loaded singletons so importing this module is cheap.
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Load all-MiniLM-L6-v2 once (local, no API key). 384-dim embeddings."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def _client() -> chromadb.ClientAPI:
    # PersistentClient writes the index to disk so we don't re-embed every run.
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


# Human-readable titles so syllabus chunks carry their course identity.
SOURCE_TITLES = {
    "foundations_of_cybersecurity.pdf": "Foundations of Cybersecurity",
    "fundamentals_database_managemnet_systems.pdf": "Fundamentals of Database Systems",
}


def embed_text(chunk: dict) -> str:
    """Build the text we EMBED (not the stored document).

    Prepends identifying context (professor, course, document title) so a query
    naming a professor or course locks onto the right source instead of any
    chunk that merely shares a topic (planning.md Anticipated Challenge #2).
    """
    md = chunk["metadata"]
    head = []
    if md.get("professor"):
        head.append(f"Professor: {md['professor']}")
    title = SOURCE_TITLES.get(md.get("source", ""))
    course = " ".join(p for p in (md.get("course_code"), title) if p)
    if course:
        head.append(f"Course: {course}")
    if md.get("section"):
        head.append(f"Section: {md['section']}")
    prefix = " — ".join(head)
    return f"{prefix}\n{chunk['text']}" if prefix else chunk["text"]


def get_collection():
    """Return the collection, creating it if needed (cosine distance)."""
    # hnsw:space=cosine -> distance = 1 - cosine_similarity (0 = identical).
    # Cosine fits normalized sentence embeddings and matches the <0.5 checkpoint
    # target better than Chroma's default squared-L2.
    return _client().get_or_create_collection(
        name=COLLECTION, metadata={"hnsw:space": "cosine"}
    )


def embed_and_store() -> None:
    """Load chunks.json, embed every chunk, and store all of them in ChromaDB."""
    chunks = json.loads(CHUNKS.read_text(encoding="utf-8"))
    model = get_model()
    client = _client()

    # Drop any existing collection so re-runs don't duplicate or mix stale data.
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    coll = client.create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})

    ids = [c["id"] for c in chunks]
    docs = [c["text"] for c in chunks]                 # stored document (clean text)
    metas = [c["metadata"] for c in chunks]            # professor, course_code, source, type, section
    embed_inputs = [embed_text(c) for c in chunks]     # context-enriched text we embed

    # normalize_embeddings=True pairs with cosine space.
    embeddings = model.encode(
        embed_inputs, normalize_embeddings=True, show_progress_bar=True
    ).tolist()

    coll.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)
    print(f"Stored {coll.count()} chunks in '{COLLECTION}' "
          f"-> {CHROMA_DIR.relative_to(ROOT)}")


def retrieve(query: str, k: int = 5) -> list[dict]:
    """Return the top-k chunks for a query, with metadata and distance score."""
    coll = get_collection()
    model = get_model()
    q_emb = model.encode([query], normalize_embeddings=True).tolist()
    res = coll.query(query_embeddings=q_emb, n_results=k)

    results = []
    for doc, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        results.append(
            {
                "text": doc,
                "distance": dist,
                "source": meta.get("source", ""),
                "professor": meta.get("professor", ""),
                "course_code": meta.get("course_code", ""),
                "section": meta.get("section", ""),
                "type": meta.get("type", ""),
            }
        )
    return results


if __name__ == "__main__":
    embed_and_store()
