from pathlib import Path
from uuid import uuid4
import fitz  # PyMuPDF

from app.models.document import (StructuredDocument, Page, Block, BoundingBox)

from .base_parser import BaseParser

class PDFParser(BaseParser):
    def parse(self, raw_document: str) -> StructuredDocument:
        """
        Parse a PDF document and return a structured document.

        Parameters
        ----------
        raw_document : str
            The path to the PDF file.

        Returns
        -------
        StructuredDocument
            The structured representation of the PDF document.
        """
        doc = fitz.open(raw_document)
        pages = []
        try:
            for page_number,page in enumerate(doc, start=1): # remove the 'r' at the end of the line
                blocks = [] #   
                for block in page.get_text("blocks"):
                    x0, y0, x1, y1, text, _, _, _ = block
                    bounding_box = BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1)
                    block_obj = Block(
                        id=str(uuid4()),
                        type="paragraph",  # Simplified; in a real scenario, you might want to classify the block type
                        text=text.strip(),
                        bounding_box=bounding_box,
                    )
                    blocks.append(block_obj)
                page_obj = Page(
                    page_number=page_number,
                    width=page.rect.width,
                    height=page.rect.height,
                    blocks=blocks,
                )
                pages.append(page_obj)
