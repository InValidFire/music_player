from .spotifysong import SpotifySong

class SpotifyAlbum:
    def __init__(self, data: dict) -> None:
        self._songs = self._load_tracks(data['items'])

    @property
    def songs(self):
        return self._songs

    def _load_tracks(self, song_list: list) -> list[SpotifySong]:
        output = []
        for song in song_list:
            output.append(SpotifySong(song))
        return output