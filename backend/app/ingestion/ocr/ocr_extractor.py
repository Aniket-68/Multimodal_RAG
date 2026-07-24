from typing import Any
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

    # To blocks - Convert the OCR results into a list of Block objects, each containing the extracted text and its corresponding bounding box.
    def _to_blocks(self, results:Any, context: ParserContext) -> list[Block]:
        blocks=[]
        # PaddleOCR 3.X result structure
        for result_index,  result in enumerate(results):
           data=getattr(result,'data',None) # Get the data attribute from the result object, which contains the OCR results 
           if callable(data):
                data=data() # If data is callable, call it to get the actual data
            
           if not isinstance(data,dict):
                continue # If data is not a dictionary, skip to the next result
           
           data=data.get("res",data)

           tests = data.get("rec_texts",[]) # Get the list of detected texts from the data dictionary
           boxes = data.get("rec_boxes",[]) # Get the list of bounding boxes corresponding to the detected texts
           scores = data.get("rec_scores",[]) # Get the list of confidence scores for the detected texts - it can be used to filter out low-confidence detections if needed

           for index, text in enumerate(tests):
               text=str(text).strip() # Convert the text to a string and remove leading/trailing whitespace     
               if not text:
                   continue # If the text is empty after stripping, skip to the next text
               
               score=(float(scores[index]) if index < len(scores) else None) # Get the confidence score for the current text, defaulting to 0.0 if not available

               bbox=None

               if index <len(boxes):
                   x0,y0,x1,y1=boxes[index] # Get the bounding box for the current text

                   """OCR ran on 2x rendered image, so we need to scale the bounding box back to the original page size by dividing the coordinates by 2.0 - what is 2x ? - it is the scaling factor used when rendering the image for OCR. The image was scaled up by a factor of 2 to improve OCR accuracy, so the bounding box coordinates need to be scaled back down by dividing by 2.0 to match the original page size."""

                   bbox=BoundingBox(x0=x0/2.0,y0=y0/2.0,x1=x1/2.0,y1=y1/2.0) # Create a BoundingBox object with the scaled coordinates of the detected text

                   blocks.append(
                       Block(
                           id=f"page_{context.page_number}_ocr_{result_index}_{index}", # Create a unique ID for the block based on the page number, result index, and text index
                           type="paragraph", # Assuming all OCR-detected blocks are paragraphs; this can be enhanced to detect headings, lists, etc. by Layout analysis or NLP techniques.
                           text=text, # Set the extracted text for the block
                           bbox=bbox, # Set the bounding box for the block
                           
                           metadata={"source": "ocr", "confidence": score},  # Include the confidence score in the metadata if available

                   )
                     )

       
               
        return blocks