"""Milestone 4 — Test retrieval against the evaluation plan queries.

Run after embed_store.py has built the vector store:
  .venv\\Scripts\\python.exe test_retrieval.py
"""
from embed_store import retrieve

K = 5
TARGET_DISTANCE = 0.5  # checkpoint: top result should be below this

# The 5 questions from planning.md's Evaluation Plan.
QUERIES = [
    "How are the group projects in CSCE 3444 instructed by Hadiseh Gooran?",
    "What are the file upload rules for assignments?",
    "How lenient is Jonathan Doran as a grader?",
    "What is Bahareh Dorri's teaching style like?",
    "How are grades divided among categories in Fundamentals of Database Systems?",
]


def main() -> None:
    for i, query in enumerate(QUERIES, 1):
        print("=" * 80)
        print(f"Q{i}: {query}")
        print("-" * 80)
        results = retrieve(query, k=K)
        for rank, r in enumerate(results, 1):
            snippet = " ".join(r["text"][:200].split())
            print(f"{rank}. dist={r['distance']:.3f}  source={r['source']}  "
                  f"section={r['section']!r}")
            print(f"   {snippet}")
        top = results[0]
        verdict = "OK (<0.5)" if top["distance"] < TARGET_DISTANCE else "HIGH (>=0.5)"
        print(f"\n   -> top distance {top['distance']:.3f} [{verdict}]  "
              f"source={top['source']}")
        print()


if __name__ == "__main__":
    main()
