import fitz  # PyMuPDF
import re

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def split_standards(text):
    pattern = r"(IS\s\d{1,5}(?::\d{4})?)"
    parts = re.split(pattern, text)

    standards = []

    for i in range(1, len(parts), 2):
        std_id = parts[i].replace("\n", "").strip()
        content = parts[i] + parts[i+1]

        content = re.sub(r"\s+", " ", content)

        standards.append({
            "standard_id": std_id,
            "text": content
        })

    return standards