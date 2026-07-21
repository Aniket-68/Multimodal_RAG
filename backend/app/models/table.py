from pydantic import BaseModel, Field

from typing import List, Any, Optional # Any - allows for any type of data to be accepted, providing flexibility in the model's attributes. Optional - allows for the possibility that the value may be None, indicating that the field is not required.

from app.models.common import BoundingBox

class TableModel(BaseModel):
    """Represents a table extracted from a document."""
    table_id: str  # Unique identifier for the table. This can be used to reference the table in other parts of the system.
    page_number: int  # The page number in the document where the table is located. This helps in identifying the position of the table within the document.
    bbox:BoundingBox  # The bounding box of the table on the page. This defines the area of the page that the table occupies.

    header: list[str] = Field(default_factory=list)  # An optional list of strings representing the header row of the table. If the table has a header, this field will contain the column names; otherwise, it will be None.

    rows: list[list[Any]] = Field(default_factory=list)  # A list of rows, where each row is a list of cell values. This represents the actual data contained in the table.

    metadata: Optional[dict] = Field(default_factory=dict)  # A dictionary to store any additional metadata related to the table. This can include information such as the source of the table, number of rows and columns, or any other relevant attributes.