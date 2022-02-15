import os, time
from pathlib import Path
import traceback
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

    def queue_item(self, uri: str):
        uri = Path(uri)
        if uri.is_file():
            song = FileSong(uri)
            self.queue.append(song)
        elif uri.is_dir():
            for file in uri.glob("**/*.mp3"):
                song = FileSong(file.resolve())
                self.queue.append(song)
        else:
            raise ValueError("Unrecognized path given.")

    def play_item(self, uri: str):
        uri = Path(uri)
        if uri.is_dir():
            for file in uri.glob("**/*.mp3"):
                song = FileSong(file.resolve())
                self.queue.insert(self.pos + 1, song)
        elif uri.is_file():
            song = FileSong(uri.resolve())
            self.queue.insert(self.pos + 1, song)
        else:
            raise ValueError("Unrecognized path given.")
        if not self.playing:
            self.toggle_playback()
        else:
            self.next_song()

    def clear_queue(self):
        if len(self.queue) > 1:
            song = self.queue[self.pos]
            self.queue.clear()
            self.queue.append(song)

    def list_queue(self):
        print("-"*os.get_terminal_size().columns)
        print(f"Song Queue ({len(self.queue)} songs): ")
        for i in range(self.pos, min(self.pos + 5, len(self.queue))):
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
            try:
                time.sleep(1)  # keeps thread from over-working
                if self.playing and not mixer.music.get_busy() and len(self.queue)-1 > self.pos:
                    self.pos += 1  # automatically move to the next song after finished playing.
                    mixer.music.load(self.queue[self.pos].path)
                    mixer.music.play()
                if self._closing:
                    break
            except:
                print("Exception in player thread. Closing.")
                traceback.print_exc()
                self.stop()