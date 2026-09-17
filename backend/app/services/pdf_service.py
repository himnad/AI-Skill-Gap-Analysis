import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from every page of a PDF.

    Returns:
        Combined text from all pages.
    """
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(
                x_tolerance=2,
                y_tolerance=2,
            )
            if page_text:
                text += page_text + "\n"

    return text.strip()