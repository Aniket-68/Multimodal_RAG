from pathlib import Path

from base_loader import BaseLoader
from pdf_loader import PDFLoader

from types import DocumentType
# pyrefly: ignore [missing-import] 


class LoaderFactory:
    """
  Factory responsible for returning the correct loader
    based on the document type.
            """
    _Loaders = {
        ".pdf": PDFLoader,
        # ".docx": DOCXLoader,
        # ".pptx": PPTXLoader,
        # ".png": ImageLoader,
    }        
    
    @classmethod
    def get_loader(cls,file_path:str) -> BaseLoader:
        """
        Returns the appropriate loader based on the file extension.
        """
        file_extension = Path(file_path).suffix.lower() # Get the file extension in lowercase
        loader_class = cls._Loaders.get(file_extension) # Get the loader class based on the file extension
        
        if not loader_class: #  If no loader class is found for the given file extension, raise a ValueError
            raise ValueError(f"No loader found for file type: {file_extension}")
        
        return loader_class(file_path) # Return an instance of the loader class initialized with the file path
    
    