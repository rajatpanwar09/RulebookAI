from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


OUTPUT = Path(__file__).resolve().parents[1] / "corpus" / "financial_regulations.pdf"


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        spaceBefore=14,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        leading=15,
        spaceAfter=8,
    )

    content = []

    content.append(
        Paragraph(
            "Financial Regulations and Fee Policy",
            title_style,
        )
    )

    sections = [
        (
            "FR-1.1",
            "Tuition Fee Deadline",
            "Students must pay the semester tuition fee by the published fee deadline. "
            "The standard deadline is listed in the university fee schedule."
        ),
        (
            "FR-2.3",
            "Late Registration",
            "A student who misses the normal registration deadline may request late "
            "registration within 10 calendar days. The request is subject to approval "
            "and payment of the applicable late registration fee."
        ),
        (
            "FR-3.2",
            "Fee Waiver",
            "Students facing documented financial hardship may apply for a partial "
            "fee waiver through the Student Welfare Office."
        ),
        (
            "FR-4.1",
            "Payment Methods",
            "University fees may be paid through the approved online payment portal "
            "or other payment methods officially announced by the Finance Office."
        ),
        (
            "FR-5.1",
            "Missed Payment Deadline",
            "Failure to pay tuition fees by the published deadline results in immediate "
            "cancellation of course registration unless an exception is approved by "
            "the designated authority."
        ),
        (
            "FR-6.2",
            "Refund Requests",
            "Refund requests must be submitted using the official Finance Office form "
            "within the applicable refund period."
        ),
    ]

    for section, heading, text in sections:
        content.append(
            Paragraph(
                f"{section} — {heading}",
                heading_style,
            )
        )
        content.append(Paragraph(text, body_style))
        content.append(Spacer(1, 5))

    doc.build(content)

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()