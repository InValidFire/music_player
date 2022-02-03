from pathlib import Path
from ..lib import Song
from mutagen.mp3 import EasyMP3

class FileSong(Song):
    def __init__(self, path: Path) -> None:
        self._path = path
        self._song = EasyMP3(path)
        self._name = ", ".join(self._load_tag('title'))
        self._length = self._load_tag('length', 0)
        self._artist = ", ".join(self._load_tag('artist'))

    def _load_tag(self, tag, error="UNKNOWN"):
        try:
            return self._song[tag]
        except KeyError:
            return error

    @property
    def name(self):
        return self._name

    @property
    def artist(self) -> str:
        return self._artist

    @property
    def length(self) -> int:
        return self._length

    @property
    def path(self) -> str:
        return self._path