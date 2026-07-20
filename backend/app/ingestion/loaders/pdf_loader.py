from pathlib import Path
import fitz

from base_loader import BaseLoader

class PDFLoader(BaseLoader):
    """ Loads a PDF using PyMuPDF. """
    def load(self, file_path: Path) -> fitz.Document:
         """
        Opens a PDF document.

        Args:
            file_path: Path to the PDF file.

        Returns:
            fitz.Document object.

        Raises:
            FileNotFoundError: If file does not exist.
            ValueError: If file is not a PDF.
            RuntimeError: If PDF cannot be opened.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"{file_path.name} is not a PDF.")

        try:
            return fitz.open(file_path)

        except Exception as e:
            raise RuntimeError(f"Unable to open PDF: {file_path}") from e

        



        
