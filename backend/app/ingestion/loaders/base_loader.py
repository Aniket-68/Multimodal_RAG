from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseLoader(ABC):
    """Base class for all document loaders."""

    @abstractmethod
    def load(self, file_path: Path) -> Any:
        """
        Load a document and return the raw document object.

        Parameters
        ----------
        file_path : Path

        Returns
        -------
        Any
        """
        raise NotImplementedError