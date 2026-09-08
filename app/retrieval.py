import os
import re
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "corpus"


# ============================================================
# TOKENIZER
# ============================================================

def tokenize(text: str):
    """
    Convert text into lowercase words.
    """
    return set(
        re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    )


# ============================================================
# READ CORPUS FILES
# ============================================================

def load_documents():
    """
    Read all .md files from the corpus directory.

    Returns:
        [
            {
                "text": "...",
                "source": "examination_policy.md"
            }
        ]
    """

    documents = []

    if not CORPUS_DIR.exists():
        return documents

    for file_path in CORPUS_DIR.glob("*.md"):

        try:
            text = file_path.read_text(
                encoding="utf-8"
            )

            if text.strip():
                documents.append({
                    "text": text,
                    "source": file_path.name
                })

        except Exception as e:
            print(
                f"Could not read {file_path}: {e}"
            )

    return documents


# ============================================================
# SPLIT MARKDOWN INTO SECTIONS
# ============================================================

def split_into_sections(text: str):
    """
    Split markdown document into sections.

    A section starts when a markdown heading is found.

    Example:

    ## EX-5.2 Plagiarism
    Plagiarism includes...

    becomes one section.
    """

    lines = text.splitlines()

    sections = []

    current_section = []

    for line in lines:

        # Support normal markdown headings:
        # ## Heading
        #
        # Also support accidentally escaped headings:
        # \## Heading

        if re.match(r"^\s*\\?#{1,6}\s+", line):

            # Save previous section
            if current_section:
                section_text = "\n".join(
                    current_section
                ).strip()

                if section_text:
                    sections.append(section_text)

            current_section = [line]

        else:
            current_section.append(line)

    # Save last section
    if current_section:

        section_text = "\n".join(
            current_section
        ).strip()

        if section_text:
            sections.append(section_text)

    return sections


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(query: str, top_k: int = 5):
    """
    Search the rulebook using simple keyword matching.

    Returns a list like:

    [
        {
            "text": "...",
            "source": "examination_policy.md",
            "score": 5
        }
    ]
    """

    documents = load_documents()

    if not documents:
        return []

    query_words = tokenize(query)

    # Remove common English words
    stop_words = {
        "what",
        "are",
        "the",
        "is",
        "a",
        "an",
        "about",
        "of",
        "to",
        "in",
        "on",
        "for",
        "and",
        "or",
        "do",
        "does",
        "how",
        "can",
        "be",
        "my",
        "me",
        "rules",
    }

    query_words = query_words - stop_words

    results = []

    for document in documents:

        text = document["text"]
        source = document["source"]

        sections = split_into_sections(text)

        # If no headings exist, search entire document
        if not sections:
            sections = [text]

        for section in sections:

            section_words = tokenize(section)

            # Basic keyword overlap
            score = len(
                query_words & section_words
            )

            # Give extra weight to words appearing
            # in the heading
            first_line = section.splitlines()[0]

            heading_words = tokenize(first_line)

            heading_score = len(
                query_words & heading_words
            )

            score += heading_score * 3

            if score > 0:

                results.append({
                    "text": section,
                    "source": source,
                    "score": score
                })

    # Sort highest score first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]