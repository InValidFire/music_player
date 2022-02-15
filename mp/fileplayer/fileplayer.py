import os, time
from pathlib import Path
import traceback
from .filesong import FileSong
from ..lib import Player
from ..lib import Queue
from os import environ
from threading import Thread

# stops "Hello from the pygame community" message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame import mixer

class FilePlayer(Player):
    def __init__(self) -> None:
        self._queue: Queue = Queue()
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
    def queue(self) -> Queue:
        return self._queue

    @property
    def playing(self) -> bool:
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

    def queue_item(self, uri: str):
        uri = Path(uri)
        if uri.is_file():
            song = FileSong(uri)
            self.queue.add(song)
        elif uri.is_dir():
            for file in uri.glob("**/*.mp3"):
                song = FileSong(file.resolve())
                self.queue.add(song)
        else:
            raise ValueError("Unrecognized path given.")

    def play_item(self, uri: str):
        uri = Path(uri)
        if uri.is_dir():
            for file in uri.glob("**/*.mp3"):
                song = FileSong(file.resolve())
                self.queue.add(song)
        elif uri.is_file():
            song = FileSong(uri.resolve())
            self.queue.add(song)
        else:
            raise ValueError("Unrecognized path given.")
        if not self.playing:
            self.toggle_playback()
        else:
            self.next_song()

    def clear_queue(self):
        if len(self.queue) > 1:
            song = self.queue.get()
            self.queue.clear()
            self.queue.add(song)

    def list_queue(self):
        print("-"*os.get_terminal_size().columns)
        print(f"Song Queue ({len(self.queue)} songs): ")
        for i in range(self.queue.pos, min(self.queue.pos + 5, len(self.queue))):
            print(self.queue.get(i))
        print("-"*os.get_terminal_size().columns)

    def next_song(self):
        mixer.music.load(self.queue.next().path)
        mixer.music.play()

    def previous_song(self):
        mixer.music.load(self.queue.previous().path)
        mixer.music.play()

    def stop(self):
        self._closing = True
        mixer.music.stop()
        mixer.music.unload()

    def thread(self):
        """Thread that manages playing the next song in the queue."""
        while True:
            try:
                time.sleep(1)  # keeps thread from over-working
                if self.playing and not mixer.music.get_busy() and not self.queue.is_empty:
                    mixer.music.load(self.queue.next().path)
                    mixer.music.play()
                if self._closing:
                    break
            except:
                print("Exception in player thread. Closing.")
                traceback.print_exc()
                self.stop()