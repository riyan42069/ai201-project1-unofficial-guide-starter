"""Extract text from the syllabus PDFs using pdfplumber.

Writes one cleaned .txt file per PDF next to the source, so the
ingestion pipeline can load them as plain text.
"""
from pathlib import Path

import pdfplumber

# Resolve paths relative to this script so it runs from any working directory.
HERE = Path(__file__).resolve().parent

# PDF source -> output .txt filename
PDFS = {
    "foundations_of_cybersecurity.pdf": "foundations_of_cybersecurity.txt",
    "fundamentals_database_managemnet_systems.pdf": "fundamentals_database_managemnet_systems.txt",
}


def extract(pdf_path: Path) -> str:
    """Return all extractable text from a PDF, one block per page."""
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n\n".join(p for p in pages if p)


def main() -> None:
    for src, out in PDFS.items():
        text = extract(HERE / src)
        (HERE / out).write_text(text, encoding="utf-8")
        print(f"{src} -> {out} ({len(text)} chars)")


if __name__ == "__main__":
    main()
