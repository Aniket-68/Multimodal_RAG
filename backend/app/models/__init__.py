from pathlib import Path
from typing import List, Optional,Literal

from pydantic import BaseModel,Field

class BoundingBox(BaseModel):
    """
    Represents a bounding box in a document.
    """
    x0: float = Field(..., description="The x-coordinate of the top-left corner of the bounding box.")
    y0: float = Field(..., description="The y-coordinate of the top-left corner of the bounding box.")
    x1: float = Field(..., description="The x-coordinate of the bottom-right corner of the bounding box.")
    y1: float = Field(..., description="The y-coordinate of the bottom-right corner of the bounding box.")

class Block(BaseModel):
    """
    Represents a single block extracted from a document.

    Examples:
        - Heading
        - Paragraph
        - Table
        - Image
    """
    id:str
    type:Literal["heading","paragraph","table","image","caption","footer","header","list","code","quote"] 
    text: Optional[str] = None
    bounding_box: Optional[BoundingBox] = None
    metadata: dict=Field(default_factory=dict)

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