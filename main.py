from pathlib import Path
import json
from types import SimpleNamespace
import traceback

from mp import FilePlayer, SpotifyPlayer

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
                args = " ".join(cmd.replace('"', '').split(" ")[1:])
                cmd = cmd.split(" ")[0]
                if not hasattr(self, "player"):
                    if cmd == "spotify":
                        self.player = SpotifyPlayer(self.settings)
                    elif cmd == "file":
                        self.player = FilePlayer()
                if cmd == "p":
                    if len(args) == 0:
                        self.player.toggle_playback()
                    else:
                        self.player.play_item(args)
                elif cmd == "e":
                    self.player.stop()
                    break
                elif cmd == "f":
                    self.player.next_song()
                elif cmd == "b":
                    self.player.previous_song()
                elif cmd == "l":
                    self.player.list_queue()
                elif cmd == "q":
                    self.player.queue_item(args)
                elif cmd == "c":
                    self.player.clear_queue()
            except NotImplementedError:
                print("This option is not available for the selected player.")
            except:
                traceback.print_exc()
                if hasattr(self, "player"):
                    self.player.stop()
                break

app = Application()