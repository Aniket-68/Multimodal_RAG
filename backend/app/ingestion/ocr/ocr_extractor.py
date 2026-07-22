import numpy as np
from paddleocr import PaddleOCR # paddleocr is a library for Optical Character Recognition (OCR) that can recognize text in images. It supports multiple languages and provides pre-trained models for text detection and recognition. difference between paddleocr and pytesseract - PaddleOCR is a deep learning-based OCR tool that uses PaddlePaddle framework, while pytesseract is a Python wrapper for Google's Tesseract-OCR Engine. PaddleOCR generally provides better accuracy and supports more languages, while pytesseract is simpler to use and integrates well with Python applications. Difference between OCR and VLM - OCR (Optical Character Recognition) is a technology that converts different types of documents, such as scanned paper documents, PDF files, or images captured by a digital camera, into editable and searchable data. VLM (Vision-Language Model) is a type of model that combines visual and textual information to understand and generate content. While OCR focuses on extracting text from images, VLMs can understand the context of both images and text, enabling tasks like image captioning, visual question answering, and multimodal content generation. 

from app.ingestion.context import ParserContext
from app.models.common import BoundingBox
from app.models.document import Block
import fitz  # PyMuPDF

class OCRExtractor:
    """
    Extracts text from images using PaddleOCR and returns a list of Block objects with the extracted text and their bounding boxes.
    """
    def __init__(self,lang:str='en'):
        """
        Initializes the OCRExtractor with a PaddleOCR instance.

        Parameters
        ----------
        lang : str, optional
            The language code for OCR (default is 'en' for English).
            # use_angle_cls=True enables angle classification, which helps in detecting the orientation of the text in the image. This is useful for images where the text may not be perfectly horizontal, allowing the OCR model to correctly recognize rotated or skewed text.
        """
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)  # Initialize PaddleOCR with angle classification and specified language

    def extract(self, context: ParserContext) -> list[Block]:
        page = context.page # Get the current page from the context
        image=page.get_pixmap(matrix=self._render_matrix(),alpha=False) # Get the image representation of the page and render it as a pixmap (bitmap image) with the specified transformation matrix and without an alpha channel (transparency).

        # Convert the image to a numpy array
        img_array=np.frombuffer(image.samples,dtype=np.uint8).reshape(image.height,image.width,image.n) # Convert the image samples to a numpy array and reshape it to the original image dimensions

        results = self.ocr.predict(img_array, cls=True)# perform OCR on the image array and get the results, with angle classification enabled

        return self._to_blocks(results, context) # Convert the OCR results to Block objects and return them
    
    def _render_matrix(self):
        """"
        2x scale improves OCR accuracy by enlarging the image, making it easier for the OCR model to detect and recognize text, especially in cases where the text is small or unclear.
        """
        return fitz.Matrix(2, 2)  # Create a transformation matrix that scales the image by a factor of 2 in both x and y directions

    
    def _to_blocks(self, results:Any, context: ParserContext) -> list[Block]:
        pass