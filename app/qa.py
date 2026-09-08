from app.retrieval import search_documents


def clean_text(text):
    if not text:
        return ""

    return (
        text
        .replace("\\##", "")
        .replace("##", "")
        .replace("\\n", "\n")
        .strip()
    )


def extract_title(text):
    """
    Extract the first meaningful line as the rule title.
    Example:
    AR-4.2 Ordinary Attendance Threshold
    """
    if not text:
        return ""

    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()

        if line:
            return clean_text(line)

    return ""


def clean_rule_body(text):
    """
    Remove the first line because it is normally the rule title.
    """
    if not text:
        return ""

    lines = text.strip().splitlines()

    # Remove empty lines at beginning
    while lines and not lines[0].strip():
        lines.pop(0)

    # First line is usually the title
    if lines:
        lines.pop(0)

    return clean_text("\n".join(lines))


def find_rule(results, keywords):
    """
    Find the first rule containing all important keywords.
    """
    for rule in results:
        text = rule.get("text", "").lower()

        if all(word.lower() in text for word in keywords):
            return rule

    return None


def build_answer(question: str):

    if not question or not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "rules": [],
            "contradictions": []
        }

    question_lower = question.lower()

    # ========================================================
    # ATTENDANCE QUESTION
    # ========================================================

    attendance_words = [
        "attendance",
        "attend",
        "present",
        "absence",
        "absent"
    ]

    is_attendance_question = any(
        word in question_lower
        for word in attendance_words
    )

    if is_attendance_question:

        # Search normal attendance rule
        normal_results = search_documents(
            "ordinary attendance threshold 75 percent examination eligibility",
            top_k=10
        )

        # Search medical exception separately
        medical_results = search_documents(
            "medical attendance exception 60 percent examination",
            top_k=10
        )

        # ----------------------------------------------------
        # Find 75% rule
        # ----------------------------------------------------

        normal_rule = None

        for rule in normal_results:

            text = rule.get("text", "").lower()

            if (
                "75 percent" in text
                or "75%" in text
            ):
                normal_rule = rule
                break

        # ----------------------------------------------------
        # Find 60% medical rule
        # ----------------------------------------------------

        medical_rule = None

        for rule in medical_results:

            text = rule.get("text", "").lower()

            if (
                ("60 percent" in text or "60%" in text)
                and "medical" in text
            ):
                medical_rule = rule
                break

        # ----------------------------------------------------
        # BOTH RULES FOUND
        # ----------------------------------------------------

        if normal_rule and medical_rule:

            normal_raw = normal_rule.get("text", "")
            medical_raw = medical_rule.get("text", "")

            normal_text = clean_rule_body(normal_raw)
            medical_text = clean_rule_body(medical_raw)

            normal_title = extract_title(normal_raw)
            medical_title = extract_title(medical_raw)

            answer = (
                "For ordinary examination eligibility, "
                "a student must have at least **75% attendance** "
                "in the relevant course.\n\n"
                "However, an important medical exception applies. "
                "A student with a documented and officially approved "
                "medical absence may be permitted to appear for the "
                "examination with attendance as low as **60%** in "
                "the affected course.\n\n"
                "**In short:**\n"
                "- Normal attendance requirement: **75%**\n"
                "- Approved medical exception: **60%**\n\n"
                "The medical documentation must be submitted through "
                "the prescribed process and approved by the competent "
                "authority."
            )

            rules = [
                {
                    "title": normal_title,
                    "text": normal_text,
                    "source": normal_rule.get("source", ""),
                    "score": normal_rule.get("score", 0)
                },
                {
                    "title": medical_title,
                    "text": medical_text,
                    "source": medical_rule.get("source", ""),
                    "score": medical_rule.get("score", 0)
                }
            ]

            sources = []

            for rule in rules:

                source = rule.get("source")

                if source and source not in sources:
                    sources.append(source)

            contradictions = [
                {
                    "type": "exception",
                    "title": "Attendance threshold exception",
                    "description": (
                        "The ordinary examination rule requires "
                        "75% attendance, while an officially approved "
                        "medical exception may allow examination "
                        "eligibility with attendance as low as 60%."
                    ),
                    "rules": [
                        normal_title,
                        medical_title
                    ]
                }
            ]

            return {
                "answer": answer,
                "sources": sources,
                "rules": rules,
                "contradictions": contradictions
            }

    # ========================================================
    # NORMAL QUESTION
    # ========================================================

    results = search_documents(
        question,
        top_k=5
    )

    if not results:

        return {
            "answer": (
                "I could not find relevant information "
                "in the university rulebook."
            ),
            "sources": [],
            "rules": [],
            "contradictions": []
        }

    best_rule = results[0]

    raw_text = best_rule.get("text", "")
    source = best_rule.get("source", "")
    title = best_rule.get("title", "")

    title = extract_title(raw_text)

    body = clean_rule_body(raw_text)

    answer = body

    rules = []
    sources = []

    for rule in results:

        raw_text = rule.get("text", "")
        source = rule.get("source", "")
        title = rule.get("title", "")

        title = extract_title(raw_text)
        body = clean_rule_body(raw_text)

        rules.append(
            {
                "title": title,
                "text": body,
                "source": source,
                "score": rule.get("score", 0)
            }
        )

        if source and source not in sources:
            sources.append(source)

    return {
        "answer": answer,
        "sources": sources,
        "rules": rules,
        "contradictions": []
    }