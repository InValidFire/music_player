from ..lib import Song

class SpotifySong(Song):
    def __init__(self, data: dict):
        print(data)
        self._name = data['name']
        self._artist = self._load_artists(data['artists'])
        self._length = data['duration_ms']
        self._path = data['external_urls']['spotify']

    @property
    def name(self):
        return self._name

    @property
    def artist(self):
        return self._artist

    @property
    def length(self):
        return self._length

    @property
    def path(self) -> str:
        return self._path

    def _load_artists(self, artist_list: list):
        names = []
        for artist in artist_list:
            names.append(artist['name'])
        return ", ".join(names)
