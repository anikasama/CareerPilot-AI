import re

import fitz


MAX_PAGES = 20


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_from_pdf(file_bytes: bytes) -> dict:
    if not file_bytes:
        raise ValueError("The uploaded PDF is empty.")

    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError("The uploaded file is not a valid PDF.") from exc

    page_count = document.page_count

    if page_count == 0:
        document.close()
        raise ValueError("The PDF does not contain any pages.")

    pages_to_read = min(page_count, MAX_PAGES)

    page_text = []

    for index in range(pages_to_read):
        page = document.load_page(index)
        text = page.get_text("text")

        if text:
            page_text.append(text)

    document.close()

    full_text = clean_text("\n".join(page_text))

    if len(full_text) < 50:
        raise ValueError(
            "Very little readable text was found in this PDF. "
            "Please upload a text-based PDF resume."
        )

    words = re.findall(r"\b[\w+#.-]+\b", full_text)

    return {
        "text": full_text,
        "pages": page_count,
        "words": len(words),
    }