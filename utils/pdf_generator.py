from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_audit_pdf(report_text: str) -> bytes:
    """
    Converts audit report text into a downloadable PDF.
    Returns PDF as bytes (in-memory).
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    story = []

    for line in report_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line.replace("&", "&amp;"), styles["Normal"]))
            story.append(Spacer(1, 8))
        else:
            story.append(Spacer(1, 12))

    doc.build(story)

    buffer.seek(0)
    return buffer.read()
