from pathlib import Path
from pypdf import PdfReader
from docx import Document


BASE_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = BASE_DIR / "data" / "notes"

NOTES_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# EXTRACT TEXT FROM PDF
# ==========================================

def extract_pdf_text(file):

    reader = PdfReader(file)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


# ==========================================
# EXTRACT TEXT FROM DOCX
# ==========================================

def extract_docx_text(file):

    document = Document(file)

    text = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


# ==========================================
# EXTRACT TEXT FROM TXT
# ==========================================

def extract_txt_text(file):

    return file.read().decode(
        "utf-8",
        errors="ignore"
    )


# ==========================================
# EXTRACT TEXT FROM ANY SUPPORTED FILE
# ==========================================

def extract_text(file):

    file_type = file.name.lower()

    if file_type.endswith(".pdf"):

        return extract_pdf_text(file)

    elif file_type.endswith(".docx"):

        return extract_docx_text(file)

    elif file_type.endswith(".txt"):

        return extract_txt_text(file)

    return ""


# ==========================================
# SAVE NOTE
# ==========================================

def save_note(filename, text):

    file_path = NOTES_DIR / filename

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)

    return file_path


# ==========================================
# GET SAVED NOTES
# ==========================================

def get_saved_notes():

    if not NOTES_DIR.exists():
        return []

    return [
        file
        for file in NOTES_DIR.iterdir()
        if file.is_file()
    ]