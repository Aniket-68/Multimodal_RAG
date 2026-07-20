# Why Extractors?
# Extractors are responsible for extracting raw data from various sources, such as files, databases,
from abc import ABC, abstractmethod
from typing import Any

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self,page:Any):
        """
        Extracts raw data from a page.

        Args:
            source (Any): The source 
            from which to extract data. This could be a file path, a database connection, etc.
            """
        raise NotImplementedError("The extract method must be implemented by subclasses.")