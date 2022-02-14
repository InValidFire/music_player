from mp.lib import Player
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyPlayer(Player):
    def __init__(self, settings) -> None:
        scopes = ['user-modify-playback-state', 'user-read-playback-state']
        auth_manager = SpotifyOAuth(scope=scopes, client_id=settings.spotify.client.id, client_secret=settings.spotify.client.secret, redirect_uri="http://localhost:9083")
        self.spotify = spotipy.Spotify(auth_manager=auth_manager)

    @property
    def playing(self):
        if self.spotify.current_playback() is not None and self.spotify.current_playback()['is_playing'] is not False:
            return True
        return False

    @property
    def queue(self) -> list:
        raise NotImplementedError("This endpoint is missing from Spotify's Web API")

    def next_song(self):
        self.spotify.next_track()

    def previous_song(self):
        self.spotify.previous_track()

    def toggle_playback(self):
        if self.playing:
            self.spotify.pause_playback()
        else:
            self.spotify.start_playback()

    def list_queue(self):
        raise NotImplementedError("This endpoint is missing from Spotify's Web API")

    def clear_queue(self):
        raise NotImplementedError("This endpoint is missing from Spotify's Web API")

    def queue_song(self, uri: str):
        if self.spotify.album_tracks(uri) is None:
            self.spotify.add_to_queue(uri)
        else:
            print(self.spotify.album_tracks(uri))
            for song in self.spotify.album_tracks(uri):
                self.spotify.add_to_queue(song)

    def stop(self):
        if self.playing:
            self.toggle_playback()