from pathlib import Path
from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Coordinates of an element on a PDF page."""
    
    x0: float
    y0: float
    x1: float
    y1: float


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

    page_number: int

    width: float

    height: float

    blocks: List[Block] = Field(default_factory=list)


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