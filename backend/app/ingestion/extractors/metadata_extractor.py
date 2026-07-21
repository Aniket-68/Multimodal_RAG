from .base_extractor import BaseExtractor
from app.models.document import ( PageMetadata )
from app.ingestion.context import ParserContext
import fitz  # PyMuPDF

class MetadataExtractor(BaseExtractor):
    def extract(self, context: ParserContext) -> PageMetadata:
        """
        Extracts metadata from a PDF page.

        Args:
            context (ParserContext): The context for parsing the document.
        """
        page=context.page  # Get the current page from the context
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