from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import re


def clean_text(text: str):
    # Remove markdown bold
    text = re.sub(r"\*\*", "", text)

    # Remove table pipes
    text = re.sub(r"\|", "", text)

    # Remove long dashes
    text = re.sub(r"-{2,}", "", text)

    # Remove ALL HTML tags (very important)
    text = re.sub(r"<[^>]+>", "", text)

    # Replace problematic unicode characters
    text = (
        text.replace("→", "->")
            .replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("`", "")
    )

    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        if line.startswith(("•", "-", "*")):
            lines.append(f"• {line[1:].strip()}")
        else:
            lines.append(line)

    return lines


def generate_pdf(activities, errors, warnings, summary):

    buffer = BytesIO()
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    story = []

    # Title
    story.append(Paragraph("<b>ICA Copilot – XAML Analysis Report</b>", styles["Title"]))
    story.append(Spacer(1, 6))

    # Activities
    story.append(Paragraph("<b>Activities</b>", styles["Heading3"]))
    for a in activities:
        story.append(Paragraph(f"• {a}", styles["BodyText"]))
    story.append(Spacer(1, 4))

    # Errors
    story.append(Paragraph("<b>Errors</b>", styles["Heading3"]))
    for e in errors:
        story.append(Paragraph(f"• {e}", styles["BodyText"]))
    story.append(Spacer(1, 4))

    # Warnings
    story.append(Paragraph("<b>Warnings</b>", styles["Heading3"]))
    for w in warnings:
        story.append(Paragraph(f"• {w}", styles["BodyText"]))
    story.append(Spacer(1, 6))

    # LLM Section
    story.append(Paragraph("<b>LLM Explanation & Suggestions</b>", styles["Heading3"]))

    cleaned = clean_text(summary)

    for line in cleaned:
        story.append(Paragraph(f"• {line}" if not line.startswith("•") else line, styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)

    return buffer