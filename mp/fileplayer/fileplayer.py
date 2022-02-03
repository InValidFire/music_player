import os
from pathlib import Path
from .filesong import FileSong
from ..lib import Player
from os import environ
from threading import Thread

# stops "Hello from the pygame community" message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame import mixer

class FilePlayer(Player):
    def __init__(self) -> None:
        self._queue: list[FileSong] = []
        self._pos: int = -1
        self._playing: bool = False
        self._closing: bool = False  # tells thread to close out when exiting
        mixer.init()
        playback_thread = Thread(target=self.thread)
        playback_thread.start()

    @property
    def pos(self) -> int:
        return self._pos

    @pos.setter
    def pos(self, new):
        if isinstance(new, int):
            self._pos = new
        else:
            raise TypeError

    @property
    def queue(self) -> list:
        return self._queue

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, b):
        if isinstance(b, bool):
            self._playing = b
        else:
            raise TypeError(b)

    def toggle_playback(self):
        if self.playing:
            self.playing = False
            mixer.music.pause()
        else:
            self.playing = True

    def queue_song(self, path: Path):
        song = FileSong(path)
        self.queue.append(song)

    def queue_dir(self, path: Path):
        if path.is_dir():
            for file in path.glob("**/*.mp3"):
                self.queue_song(file.resolve())

    def clear_queue(self):
        raise NotImplementedError

    def list_queue(self):
        print("-"*os.get_terminal_size().columns)
        print(f"Song Queue ({len(self.queue)} songs): ")
        for i in range(self.pos, self.pos + 5):
            print(self.queue[i])
        print("-"*os.get_terminal_size().columns)

    def next_song(self):
        mixer.music.stop()

    def previous_song(self):
        self.pos -= 2
        mixer.music.stop()

    def stop(self):
        self._closing = True
        mixer.music.stop()
        mixer.music.unload()

    def thread(self):
        while True:
            if self.playing and not mixer.music.get_busy():
                self.pos += 1  # automatically move to the next song after finished playing.
                mixer.music.load(self.queue[self.pos].path)
                mixer.music.play()
            if self._closing:
                break
        