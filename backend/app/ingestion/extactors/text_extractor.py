from typing import List
import fitz  # PyMuPDF

from .base_extractor import BaseExtractor
from app.models.document import ( Block, BoundingBox )

class TextExtractor(BaseExtractor):
    def extract(self, page: fitz.Page) -> List[Block]:
        """
        Extracts text blocks from a PDF page.

        Args:
            page (fitz.Page): The PDF page from which to extract text.
            # not need to open fitz, as the page is already provided
            """
        extracted_blocks:List[Block] = [] # List to hold the extracted text blocks
        blocks=page.get_text("blocks")

        for index, block in enumerate(blocks): # Iterate through each block of text
            x0, y0, x1, y1, text, *_ = block # Unpack the block information (coordinates and text)
            text = text.strip() # Remove leading and trailing whitespace from the text

            # Edge case: If the text is empty after stripping, skip this block
            if not text:
                continue
            
            extracted_blocks.append(
                Block(
                    id=f"page_{page.number}_block_{index}",
                    type="paragraph", # Assuming all blocks are paragraphs for simplicity; this can be enhanced to detect headings, lists, etc. by Layout analysis or NLP techniques.
                    text=text,
                    bbox=BoundingBox(
                        x0=x0,
                        y0=y0,
                        x1=x1,
                        y1=y1,
                    ),
                )
            )
        return extracted_blocks