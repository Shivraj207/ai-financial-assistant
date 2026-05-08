import fitz  # PyMuPDF
from typing import List, Dict


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extract text from a PDF page by page.

    Args:
        pdf_path (str): Path to PDF file

    Returns:
        List[Dict]: List of page-wise extracted text
    """

    pages = []

    try:
        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc, start=1):

            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page": page_num,
                    "text": text,
                    "source": pdf_path
                })

        doc.close()

    except Exception as e:
        print(f"[ERROR] Failed to process PDF: {e}")

    return pages