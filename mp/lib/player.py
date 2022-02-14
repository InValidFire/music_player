"""Abstract Base Class for implementation of music players."""

from abc import ABC, abstractmethod

class Player(ABC):

    @property
    @abstractmethod
    def playing(self) -> bool:
        """True if playing music, False otherwise."""
        pass

    @property
    @abstractmethod
    def queue(self) -> list:
        """List of all songs in the queue."""
        pass

    @abstractmethod
    def next_song(self):
        """Skip to the next song in the queue."""
        pass

    @abstractmethod
    def previous_song(self):
        """Go to the previous song in the queue."""
        pass

    @abstractmethod
    def toggle_playback(self):
        """Toggles playback on the music player. Starts playing if paused, and vice-versa."""
        pass

    @abstractmethod
    def list_queue(self):
        """Print the song queue to output."""
        pass

    @abstractmethod
    def clear_queue(self):
        """Remove all songs from the queue."""
        pass

    @abstractmethod
    def queue_song(self, uri):
        """Add a song to the queue."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the player."""
        pass