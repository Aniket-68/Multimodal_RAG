from pathlib import Path
from typing import List, Optional, Literal

from mlflow import Image
from pydantic import BaseModel, Field

from app.models.common import BoundingBox
from app.models.metadata import PageMetadata
from app.models.image import ImageModel
from app.models.table import TableModel



class Block(BaseModel):
    """
    Represents a single block extracted from a document.

    Examples:
        - Heading
        - Paragraph
        - Table
        - Image
    """

    id: str

    type: Literal[
        "heading",
        "paragraph",
        "table",
        "image",
        "caption",
        "footer",
        "header",
        "unknown"
    ]

    text: Optional[str] = None

    bbox: Optional[BoundingBox] = None

    metadata: dict = Field(default_factory=dict)


class Page(BaseModel):
    """Represents one page in the document."""

    metadata: PageMetadata

    blocks: List[Block] = Field(default_factory=list)

    images: List[ImageModel] = Field(default_factory=list)

    tables: List[TableModel] = Field(default_factory=list) # in short - it represents the tables extracted from the page. Each TableModel instance contains information about a single table, including its unique identifier, page number, bounding box, header, rows, and any additional metadata. This allows for structured representation and easy access to table data within the document.



class StructuredDocument(BaseModel):
    """
    Internal representation of a parsed document.
    """

    document_id: str

    file_name: str

    file_path: Path

    total_pages: int

    pages: List[Page] = Field(default_factory=list)

    metadata: dict = Field(default_factory=dict)