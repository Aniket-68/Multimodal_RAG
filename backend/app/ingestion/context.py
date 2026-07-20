from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF

@dataclass # it is a decorator that automatically generates special methods for the class, such as __init__, __repr__, and __eq__, based on the class attributes.
class ParserContext: # it is a class that holds the context for parsing a document, including the document itself, the current page being processed, and the page number. in simple words - it is a simple data structure that groups together related information needed during the parsing process.
    """
    shared context for parsing a document, including the document itself, the current page being processed, and the page number.
    """
    document:fitz.Document 
    
    page : fitz.Page 

    page_number:int
    output_dir: Path