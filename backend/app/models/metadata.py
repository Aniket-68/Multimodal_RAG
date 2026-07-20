from pydantic import BaseModel

class PageMetadata(BaseModel):
    """
    Represents metadata for a single page in a document.
    Schema for storing metadata related to a specific page in a document, such as its number, dimensions, and any additional information.
    """

    page_number: int
    width: float
    height: float
    rotation: float = 0.0  # Default rotation is 0 degrees
    has_text: bool = True  # Indicates if the page contains text
    has_images: bool = False  # Indicates if the page contains images
    has_links: bool = False  # Indicates if the page contains hyperlinks
    has_annotations: bool = False  # Indicates if the page contains annotations