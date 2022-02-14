from pathlib import Path
import json
from types import SimpleNamespace

from mp.fileplayer import FilePlayer
from mp.spotifyplayer import SpotifyPlayer

class Application:
    """Temporary application to test music player library functionality."""

    def __init__(self):
        with Path("settings.json").open("r+") as f:  # TODO: Improve settings reading
            self.settings: SimpleNamespace = json.load(f, object_hook= lambda _ : SimpleNamespace(**_))
        self._start()

    def _start(self):  # TODO: Improve client interface
        """Start the Application Client"""
        while True:
            try:
                cmd = input("Enter command: ")
                if not hasattr(self, "player"):
                    if cmd == "spotify":
                        self.player = SpotifyPlayer(self.settings)
                    elif cmd == "file":
                        self.player = FilePlayer()
                if cmd == "p":
                    self.player.toggle_playback()
                elif cmd == "e":
                    self.player.stop()
                    break
                elif cmd == "f":
                    self.player.next_song()
                elif cmd == "b":
                    self.player.previous_song()
                elif cmd == "l":
                    self.player.list_queue()
                elif cmd.split(" ")[0] == "q":
                    self.player.queue_song(cmd.split(" ")[1])
            except NotImplementedError:
                print("This option is not available for the selected player.")

app = Application()