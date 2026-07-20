from abc import ABC, abstractmethod
from app.models.document import structuredDocument

class BaseParser(ABC):
    @abstractmethod
    def parse(self, raw_document) -> structuredDocument:
        """
        Parse a raw document and return a structured document.

        Parameters
        ----------
        raw_document : Any

        Returns
        -------
        structuredDocument
        """
        pass
