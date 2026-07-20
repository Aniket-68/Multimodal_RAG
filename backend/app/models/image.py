from pathlib import Path
from typing import Optional 
# Optional - allows for the possibility that the value may be None, indicating that the field is not required.

from pydantic import BaseModel

class ImageModel(BaseModel): 
    """
    Represents an image extracted from a document.
    Schema for storing information about an image, including its URL, dimensions, and any additional metadata.
    """

    image_id:str # Unique identifier for the image. This can be used to reference the image in other parts of the system.

    page_number: int # The page number in the document where the image is located. This helps in identifying the position of the image within the document.

    file_path: Path # The file path where the image is stored. This can be a local path or a URL, depending on how the images are managed in the system.

    width:Optional[int] = None # Width of the image in pixels
    
    height:Optional[int] = None # Height of the image in pixels
    
    extension: str # The file extension of the image (e.g., 'jpg', 'png').
    
    metadata: dict = {} # metadata: A dictionary to store any additional metadata related to the image. This can include information such as the source of the image, copyright details, or any other relevant attributes.