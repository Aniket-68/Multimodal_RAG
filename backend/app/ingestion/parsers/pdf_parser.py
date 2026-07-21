from pathlib import Path
from uuid import uuid4

import fitz # PyMuPDF

from app.models.document import (
    StructuredDocument,
    Page
)
from app.ingestion.extractors.text_extractor import TextExtractor
from app.ingestion.extractors.metadata_extractor import MetadataExtractor
from app.ingestion.extractors.image_extractor import ImageExtractor
from app.ingestion.extractors.table_extractor import TableExtractor
from .base_parser import BaseParser
from app.ingestion.context import ParserContext

class PDFParser(BaseParser):
    """
    Parses PDF documents into StructuredDocument.
    """
    # Class constructor that takes a TextExtractor instance as an argument
    def __init__(self, text_extractor: TextExtractor, metadata_extractor: MetadataExtractor, image_extractor: ImageExtractor, table_extractor: TableExtractor = None):
        self.text_extractor = text_extractor
        self.metadata_extractor = metadata_extractor
        self.image_extractor = image_extractor
        self.table_extractor = table_extractor  # Initialize table_extractor to the provided instance or None if not provided   


    def parse(self, file_path: Path) -> StructuredDocument:

        pdf = fitz.open(file_path) # Open the PDF file using PyMuPDF

        pages = [] # List to hold the parsed pages

        try:

            for page_number, page in enumerate(pdf, start=1):

                # Notice how PDFParser no longer knows how text is extracted. It simply coordinates the workflow.
                # The parser remains an orchestrator, while each extractor owns a single responsibility. This architecture is easier to extend, test, and maintain as the project grows.
                context = ParserContext(
                    document=pdf,   
                    page=page,
                    page_number=page_number,
                    output_dir=self.image_extractor.output_dir )  # Pass the output directory to the context for image extraction)


                text_blocks = self.text_extractor.extract(context) # Extract text blocks from the page
                metadata = self.metadata_extractor.extract(context) # Extract metadata from the page
                images = self.image_extractor.extract(context) # Extract images from the page
                tables = self.table_extractor.extract(context)   # Extract tables from the page if table_extractor is provided

                pages.append(
                    Page(
                        metadata=metadata,
                        blocks=text_blocks,
                        images=images,  
                        tables=tables,  # Add the extracted tables to the Page model
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