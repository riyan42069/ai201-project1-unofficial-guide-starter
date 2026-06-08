"""Milestone 3 — Ingestion and chunking for The Unofficial Guide.

Pipeline (per planning.md):
  Raw docs (.txt reviews, .pdf syllabi)
    -> Ingestion (plain-text load for .txt, pdfplumber for .pdf)
    -> Cleaning (strip link artifacts, page numbers, whitespace)
    -> Chunking (record-level for RMP reviews, section-level for syllabi)
    -> Metadata (professor, course_code, source, type, section)
    -> data/chunks/chunks.json

Document types
  - RMP reviews:  documents/*_rmp.txt  -> one chunk per review (split on '---')
  - Syllabi:      documents/*.pdf      -> one chunk per section header

Note: documents/ also holds .txt files extracted from the syllabus PDFs.
Those are skipped here so the syllabi are not ingested twice — the PDFs are
the source of record (loaded with pdfplumber as the spec requires).
"""
import json
import random
import re
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "documents"
OUT = ROOT / "data" / "chunks" / "chunks.json"

# Chunking strategy (planning.md): no overlap; 500-token ceiling per chunk.
TOKEN_CEILING = 500

# Small words ignored when judging whether a line is "title case".
SMALL_WORDS = {
    "a", "an", "the", "and", "or", "of", "in", "on", "for", "with", "to",
    "as", "at", "by", "via", "this", "your", "our", "my",
}


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------
def load_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_pdf(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n\n".join(p for p in pages if p)


# --------------------------------------------------------------------------
# Cleaning
# --------------------------------------------------------------------------
def clean_text(text: str) -> str:
    """Remove link artifacts, Canvas noise, page numbers, and stray whitespace."""
    # Drop parenthetical links: (https://...), (http://...), (mailto:...), (tel:...)
    text = re.sub(r"\((?:https?://|mailto:|tel:)[^)]*\)", "", text)
    # Drop the repeated Canvas export phrase.
    text = re.sub(r"Links to an external site\.?", "", text)
    # Drop any remaining bare URLs.
    text = re.sub(r"https?://\S+", "", text)

    out_lines: list[str] = []
    for raw in text.splitlines():
        line = re.sub(r"[ \t]{2,}", " ", raw.rstrip())
        stripped = line.strip()
        # Drop empty Canvas "Edit" affordance lines but keep paragraph breaks.
        if stripped in ("", "Edit"):
            out_lines.append("")
            continue
        # Drop lone page numbers / "Page X of Y".
        if re.fullmatch(r"(Page\s*)?\d+(\s*of\s*\d+)?", stripped, flags=re.I):
            continue
        out_lines.append(stripped)

    cleaned = "\n".join(out_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)  # collapse blank-line runs
    return cleaned.strip()


# --------------------------------------------------------------------------
# Token estimate (rough: ~4 chars/token, good enough for a ceiling check)
# --------------------------------------------------------------------------
def est_tokens(text: str) -> int:
    return max(1, len(text) // 4)


# --------------------------------------------------------------------------
# RMP review chunking — split on '---' separators, one review per chunk
# --------------------------------------------------------------------------
def chunk_reviews(text: str, source: str) -> list[dict]:
    text = clean_text(text)
    parts = re.split(r"\n\s*-{3,}\s*\n", text)

    header = parts[0]
    m = re.search(r"^Professor:\s*(.+)$", header, flags=re.M)
    professor = m.group(1).strip() if m else ""

    chunks: list[dict] = []
    for block in parts[1:]:
        block = re.sub(r"\s+", " ", block).strip()  # reflow wrapped lines
        if not block:
            continue
        m = re.search(r"Course:\s*([A-Z]{2,4}\s*\d{3,4})", block)
        course_code = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        chunks.append(
            {
                "text": block,
                "metadata": {
                    "professor": professor,
                    "course_code": course_code,
                    "source": source,
                    "type": "review",
                    "section": "",
                },
            }
        )
    return chunks


# --------------------------------------------------------------------------
# Syllabus chunking — split on section headers
# --------------------------------------------------------------------------
def is_header(line: str) -> bool:
    s = line.strip()
    if not s or len(s) > 70:
        return False
    if not s[0].isupper():
        return False
    if s[-1] in ".,:;?!":          # headers don't end in sentence punctuation
        return False
    if s.endswith(")") or "http" in s or "@" in s or "%" in s:
        return False
    words = s.split()
    if len(words) > 8:
        return False
    cap = total = 0
    for w in words:
        wl = w.strip("“”\"'").lower()
        if wl in SMALL_WORDS:
            continue
        total += 1
        if w[0].isupper() or w[0].isdigit():
            cap += 1
    return total > 0 and cap / total >= 0.8


def split_oversized(title: str, body: str) -> list[str]:
    """Keep a section under the token ceiling, splitting on paragraphs/sentences."""
    full = f"{title}\n{body}".strip()
    if est_tokens(full) <= TOKEN_CEILING:
        return [full]

    pieces: list[str] = []
    buf = title  # repeat the title on each sub-chunk so it stays self-contained
    for para in re.split(r"\n\s*\n", body):
        para = para.strip()
        if not para:
            continue
        candidate = f"{buf}\n{para}".strip()
        if est_tokens(candidate) > TOKEN_CEILING and buf != title:
            pieces.append(buf.strip())
            buf = f"{title}\n{para}"
        else:
            buf = candidate
    if buf.strip() and buf.strip() != title:
        pieces.append(buf.strip())
    return pieces or [full]


def chunk_syllabus(text: str, source: str) -> list[dict]:
    cleaned = clean_text(text)

    m = re.search(r"CSCE\s*(\d{4})", cleaned)
    course_code = f"CSCE {m.group(1)}" if m else ""
    m = re.search(r"^Name:\s*(.+)$", cleaned, flags=re.M)
    professor = re.sub(r"\(.*?\)", "", m.group(1)).strip() if m else ""

    # Group lines into (title, body) sections, merging multi-line headers.
    # A wrapped header spans at most 2 lines; a longer run of header-like
    # lines is really a link/label list (e.g. "Student Support Services"),
    # so we cap merging and later drop any title-only section.
    sections: list[tuple[str, list[str]]] = []
    title, body, merged = "", [], False
    for line in cleaned.splitlines():
        if is_header(line):
            if title and not body and not merged:
                title = f"{title} {line.strip()}".strip()
                merged = True
            else:
                if title or body:
                    sections.append((title, body))
                title, body, merged = line.strip(), [], False
        else:
            body.append(line)
    if title or body:
        sections.append((title, body))

    chunks: list[dict] = []
    for sec_title, sec_lines in sections:
        body_text = "\n".join(sec_lines).strip()
        if not body_text:  # drop title-only sections (mis-detected list labels)
            continue
        for piece in split_oversized(sec_title, body_text):
            if not piece.strip():
                continue
            chunks.append(
                {
                    "text": piece,
                    "metadata": {
                        "professor": professor,
                        "course_code": course_code,
                        "source": source,
                        "type": "syllabus",
                        "section": sec_title,
                    },
                }
            )
    return chunks


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------
def main() -> None:
    all_chunks: list[dict] = []

    review_files = sorted(DOCS.glob("*_rmp.txt"))
    pdf_files = sorted(DOCS.glob("*.pdf"))

    for path in review_files:
        all_chunks.extend(chunk_reviews(load_txt(path), path.name))

    for path in pdf_files:
        all_chunks.extend(chunk_syllabus(load_pdf(path), path.name))

    # Assign stable ids.
    for i, chunk in enumerate(all_chunks):
        chunk["id"] = f"chunk-{i:04d}"
        chunk["tokens"] = est_tokens(chunk["text"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    n_review = sum(c["metadata"]["type"] == "review" for c in all_chunks)
    n_syllabus = sum(c["metadata"]["type"] == "syllabus" for c in all_chunks)
    over = [c["id"] for c in all_chunks if c["tokens"] > TOKEN_CEILING]
    print(f"Loaded {len(review_files)} review files + {len(pdf_files)} PDFs")
    print(f"Wrote {len(all_chunks)} chunks -> {OUT.relative_to(ROOT)}")
    print(f"  reviews:  {n_review}")
    print(f"  syllabus: {n_syllabus}")
    print(f"  over {TOKEN_CEILING}-token ceiling: {len(over)}")

    # Inspect 5 random chunks.
    print("\n=== 5 random chunks ===")
    for chunk in random.sample(all_chunks, min(5, len(all_chunks))):
        md = chunk["metadata"]
        print(f"\n[{chunk['id']}] tokens~{chunk['tokens']} type={md['type']} "
              f"source={md['source']}")
        print(f"  professor={md['professor']!r} course_code={md['course_code']!r} "
              f"section={md['section']!r}")
        text = chunk["text"]
        print("  text:", (text[:500] + " ...") if len(text) > 500 else text)


if __name__ == "__main__":
    main()
