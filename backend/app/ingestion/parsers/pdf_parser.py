from pathlib import Path
from uuid import uuid4

import fitz # PyMuPDF

from app.models.document import (
    StructuredDocument,
    Page
)
from app.ingestion.extractors.text_extractor import TextExtractor

from .base_parser import BaseParser


class PDFParser(BaseParser):
    """
    Parses PDF documents into StructuredDocument.
    """
    # Class constructor that takes a TextExtractor instance as an argument
    def __init__(self, text_extractor: TextExtractor):
        self.text_extractor = text_extractor
        

    def parse(self, file_path: Path) -> StructuredDocument:

        pdf = fitz.open(file_path) # Open the PDF file using PyMuPDF

        pages = [] # List to hold the parsed pages

        try:

            for page_number, page in enumerate(pdf, start=1):

                # Notice how PDFParser no longer knows how text is extracted. It simply coordinates the workflow.
                # The parser remains an orchestrator, while each extractor owns a single responsibility. This architecture is easier to extend, test, and maintain as the project grows.
                text_blocks = self.text_extractor.extract(page) # Extract text blocks from the page

                pages.append(
                    Page(
                        page_number=page_number,
                        width=page.rect.width,
                        height=page.rect.height,
                        blocks=text_blocks,
                    )
                )

        finally:
            pdf.close()

        return StructuredDocument(
            document_id=str(uuid4()),
            file_name=file_path.name,
            file_path=file_path,
            total_pages=len(pages),
            pages=pages,
        )