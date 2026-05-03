import fitz  # PyMuPDF
import re

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def split_standards(text):
    # Match full standard ID WITH year (and optional Part)
    pattern = r"(IS\s*\d{1,5}(?:\s*\(Part\s*\d+\))?\s*:\s*\d{4})"

    matches = list(re.finditer(pattern, text))

    standards = []

    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)

        # Clean ID
        std_id = matches[i].group()
        std_id = re.sub(r"\s+", " ", std_id).strip()

        # Extract content safely
        content = text[start:end]
        content = re.sub(r"\s+", " ", content).strip()

        # Safety check (avoid empty or broken entries)
        if std_id:
            standards.append({
                "standard_id": std_id,
                "text": content
            })

    return standards