from pathlib import Path
from uuid import uuid4

import fitz # PyMuPDF

from app.models.document import (
    StructuredDocument,
    Page,
    Block,
    BoundingBox,
)

from .base_parser import BaseParser


class PDFParser(BaseParser):
    """
    Parses PDF documents into StructuredDocument.
    """

    def parse(self, file_path: Path) -> StructuredDocument:

        pdf = fitz.open(file_path) # Open the PDF file using PyMuPDF

        pages = [] # List to hold the parsed pages

        try:

            for page_number, page in enumerate(pdf, start=1):

                page_blocks = [] # List to hold the blocks of text for the current page

                blocks = page.get_text("blocks") # Get the text blocks from the page

                for index, block in enumerate(blocks): # Iterate through each block of text

                    x0, y0, x1, y1, text, *_ = block # Unpack the block information (coordinates and text)

                    text = text.strip() # Remove leading and trailing whitespace from the text

                    # Edge case: If the text is empty after stripping, skip this block
                    if not text:
                        continue
                    
                    page_blocks.append(
                        Block(
                            id=f"page_{page_number}_block_{index}",
                            type="paragraph",
                            text=text,
                            bbox=BoundingBox(
                                x0=x0,
                                y0=y0,
                                x1=x1,
                                y1=y1,
                            ),
                        )
                    )

                pages.append(
                    Page(
                        page_number=page_number,
                        width=page.rect.width,
                        height=page.rect.height,
                        blocks=page_blocks,
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