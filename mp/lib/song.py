"""Abstract Base Class for implementing Song metadata access."""

from abc import ABC, abstractmethod

class Song(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the song."""
        pass

    @property
    @abstractmethod
    def length(self) -> int:
        """Length of the song (in seconds)."""
        pass

    @property
    @abstractmethod
    def artist(self) -> str:
        """Artist(s) of the song."""
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        """Path for the song, could also be a URI."""
        pass

    def __str__(self):
        return f"{self.name} | {self.artist}"
