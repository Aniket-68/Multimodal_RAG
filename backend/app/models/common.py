from pydantic import BaseModel


class BoundingBox(BaseModel):
    """Coordinates of an element on a PDF page."""
    
    x0: float
    y0: float
    x1: float
    y1: float

