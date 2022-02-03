from os import environ
from pathlib import Path

from mp.fileplayer import FilePlayer

if __name__ == "__main__":
    player = FilePlayer()
    player.queue_dir(Path("C:/Users/Riley/Music/AJR"))
    player.list_queue()
    player.toggle_playback()
    while True:
        cmd = input("Enter command: ")
        if cmd == "p":
            player.toggle_playback()
        elif cmd == "e":
            player.stop()
            break
        elif cmd == "f":
            player.next_song()
        elif cmd == "b":
            player.previous_song()
        elif cmd == "l":
            player.list_queue()