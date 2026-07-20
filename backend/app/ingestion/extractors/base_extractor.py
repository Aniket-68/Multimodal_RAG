# Why Extractors?
# Extractors are responsible for extracting raw data from various sources, such as files, databases,
from abc import ABC, abstractmethod
from typing import Any
from app.ingestion.context import ParserContext

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, context: ParserContext):
        """
        Extracts raw data from a page.

        Args:
            context (ParserContext): The context for parsing the document.

        Returns:
            Any: The extracted data.
        """
        raise NotImplementedError("The extract method must be implemented by subclasses.")