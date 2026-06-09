"""Milestone 5 — Grounded generation over retrieved chunks (Groq).

Pipeline stage (per planning.md):
  retrieve() -> build context -> Groq llama-3.3-70b-versatile (grounded)
             -> answer + programmatic source attribution

Grounding is enforced in the SYSTEM prompt (answer ONLY from context, else an
exact refusal string). Source attribution is built in Python from the retrieved
chunks' metadata — the model is explicitly told NOT to cite sources itself.
"""
import os

from dotenv import load_dotenv
from groq import Groq

from embed_store import retrieve

load_dotenv()  # read GROQ_API_KEY from .env (never hardcode the key)

MODEL = "llama-3.3-70b-versatile"
# retrieve() reranks a larger candidate pool with a cross-encoder, so a small K
# still captures the most relevant chunks (no need to over-retrieve into noise).
K = 5
SOURCE_DISTANCE_MAX = 0.6  # only use/cite chunks whose bi-encoder distance is this close
REFUSAL = "I don't have enough information on that."

SYSTEM_PROMPT = (
    "You are a factual assistant for an Unofficial Guide to University of North "
    "Texas CSCE professors and courses. Follow these rules strictly:\n"
    "1. Answer using ONLY the information in the context documents provided in "
    "the user message. Do not use any outside or prior knowledge.\n"
    "2. Use whatever relevant details the context contains, even if they are "
    "brief, scattered, or mixed. Student comments about a professor's lectures, "
    "explanations, examples, quizzes, grading, helpfulness, or classroom "
    "approach all describe that professor — summarize them, and when opinions "
    "differ, report the range of views. You may and should synthesize and "
    "summarize across multiple reviews to characterize the professor; combining "
    "what the reviews say is expected and does NOT count as outside knowledge.\n"
    "3. Reply with the refusal sentence ONLY when the context contains no "
    "information related to the question. The refusal must be EXACTLY this "
    f"sentence and nothing else: \"{REFUSAL}\"\n"
    "4. Do not add any fact or opinion that is not stated in the context.\n"
    "5. Do not mention, list, or cite sources in your answer — source "
    "attribution is added separately by the system."
)

_client: Groq | None = None


def _groq() -> Groq:
    global _client
    if _client is None:
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your .env file as "
                "GROQ_API_KEY=your_key_here"
            )
        _client = Groq(api_key=key)
    return _client


def _format_context(chunks: list[dict]) -> str:
    return "\n\n---\n\n".join(c["text"] for c in chunks)


def _source_label(chunk: dict) -> str:
    """Human-readable attribution for one chunk, derived from its metadata."""
    src = chunk.get("source", "")
    extra = chunk.get("professor") if chunk.get("type") == "review" else chunk.get("course_code")
    return f"{src} ({extra})" if extra else src


def ask(question: str, k: int = K) -> dict:
    """Return {"answer": str, "sources": list[str]} grounded in retrieved chunks."""
    retrieved = retrieve(question, k=k)
    # Recall via a generous K, precision via a distance band: only chunks close
    # enough to be relevant reach the model (and get cited), so a high K doesn't
    # feed it loosely-related noise. Fall back to the closest few so a genuinely
    # out-of-scope query still gets seen (and refused).
    chunks = [c for c in retrieved if c.get("distance", 1.0) <= SOURCE_DISTANCE_MAX]
    if not chunks:
        chunks = retrieved[:3]

    user_msg = (
        "Context documents:\n"
        f"{_format_context(chunks)}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above."
    )

    resp = _groq().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,  # deterministic, less room to drift off-context
    )
    answer = resp.choices[0].message.content.strip()

    # Programmatic attribution: build the source list from retrieved metadata,
    # deduplicated by filename. Only cite sources whose chunk is close enough to
    # be relevant (drops loosely-related docs pulled in by the generous K). Skip
    # entirely when the model refused (no grounded answer = no sources to claim).
    if REFUSAL.lower() in answer.lower():
        sources: list[str] = []
    else:
        seen, sources = set(), []
        for c in chunks:  # already distance-filtered above
            src = c.get("source", "")
            if src and src not in seen:
                seen.add(src)
                sources.append(_source_label(c))

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "How lenient is Jonathan Doran as a grader?"
    out = ask(q)
    print("Q:", q)
    print("\nANSWER:\n", out["answer"])
    print("\nSOURCES:")
    for s in out["sources"]:
        print("  -", s)
