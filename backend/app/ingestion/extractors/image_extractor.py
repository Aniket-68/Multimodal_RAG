from pathlib import Path # shorthand for "path to a file or directory"
from uuid import uuid4 # generates a unique identifier

import fitz  # PyMuPDF
from PIL import image # Python Imaging Library, used for opening, manipulating, and saving many different image file formats


from .base_extractor import BaseExtractor
from app.models.image import ImageModel


class ImageExtractor(BaseExtractor):
    
    def __init__(self,output_dir: Path):
        """
        Initializes the ImageExtractor.

        Args:
            output_dir (Path): The directory where extracted images will be saved.
        """
        self.output_dir = output_dir # it is a Path object representing the directory where extracted images will be saved
        self.output_dir.mkdir(parents=True, exist_ok=True)  # Create the output directory if it doesn't exist

    def extract(self, pdf: fitz.Document, page: fitz.Page) -> list[ImageModel]:
        """
        Extracts images from a PDF page.

        Args:
            pdf (fitz.Document): The PDF document.
            page (fitz.Page): The PDF page from which to extract images.
        """

        extracted_images: list[ImageModel] = []  # List to hold the extracted images

        images = page.get_images(full=True)  # Get all images on the page , full =True means to get all images, including those that are not directly visible on the page (e.g., images that are part of annotations or form fields).

        for img_index, img in enumerate(images):  # Iterate through each image on the page
            xref = img[0] # The xref (cross-reference) number of the image in the PDF
           

        
            base_image = pdf.extract_image(xref)  # Extract the image using its xref
            image_bytes = base_image["image"]  # Get the image bytes
            image_extension = base_image["ext"]  # Get the image extension (e.g., 'png', 'jpg')

            # Generate a unique filename for the extracted image
            image_id = str(uuid4())
            image_filename = f"{image_id}.{image_extension}"
            image_path = self.output_dir / image_filename  # Full path to save the image

            # Save the extracted image to the specified output directory
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            # Open the saved image to get its dimensions
            with open(image_path) as img_obj: # it is a file object representing the saved image, which can be used to read the image data.
                img_obj = image.open(img_obj) # it is a PIL Image object representing the opened image, which can be used to access image properties and perform image processing tasks.    
                width, height = img_obj.size

            # Create an ImageModel instance for the extracted image
            extracted_images.append(
                ImageModel(
                    image_id=image_id,
                    page_number=page.number,
                    file_path=image_path,
                    width=width,
                    height=height,
                    extension=image_extension,
                    metadata={},  # You can add any additional metadata here if needed
                )
            )


       