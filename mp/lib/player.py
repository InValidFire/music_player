"""Abstract Base Class for implementation of music players."""

from abc import ABC, abstractmethod

class Player(ABC):

    @property
    @abstractmethod
    def playing(self) -> bool:
        pass

    @property
    @abstractmethod
    def queue(self) -> list:
        pass

    @abstractmethod
    def next_song(self):
        pass

    @abstractmethod
    def previous_song(self):
        pass

    @abstractmethod
    def toggle_playback(self):
        pass

    @abstractmethod
    def list_queue(self):
        pass

    @abstractmethod
    def clear_queue(self):
        pass

