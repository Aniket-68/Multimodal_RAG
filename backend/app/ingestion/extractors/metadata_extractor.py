from .base_extractor import BaseExtractor
from app.models.document import ( PageMetadata )
import fitz  # PyMuPDF

class MetadataExtractor(BaseExtractor):
    def extract(self, page: fitz.Page) -> PageMetadata:
        """
        Extracts metadata from a PDF page.

        Args:
            page (fitz.Page): The PDF page from which to extract metadata.
        """
        return PageMetadata(
            page_number=page.number+1,
            width=page.rect.width,
            height=page.rect.height,
            rotation=page.rotation,
            has_text=bool(page.get_text("text").strip()),
            has_images=bool(page.get_images(full=True)),
            has_links=bool(page.get_links()),
            has_annotations=bool(page.annots()),
                
        )