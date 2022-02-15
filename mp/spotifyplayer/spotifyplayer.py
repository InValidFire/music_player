from mp.lib import Player
from .spotifyalbum import SpotifyAlbum
from .spotifyplaylist import SpotifyPlaylist
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

    def queue_item(self, uri: str):
        if 'playlist' in uri:
            playlist = SpotifyPlaylist(self.spotify.playlist_tracks(uri))
            for song in playlist.songs:
                self.spotify.add_to_queue(song.path)
        elif 'album' in uri:
            album = SpotifyAlbum(self.spotify.album_tracks(uri))
            for song in album.songs:
                self.spotify.add_to_queue(song.path)
        elif 'song' in uri:
            self.spotify.add_to_queue(uri)
        else:
            raise ValueError("Unknown item given to queue.")

    def play_item(self, uri: str):
        if "track" in uri:
            self.spotify.start_playback(uris=uri)
        else:
            self.spotify.start_playback(context_uri=uri)

    def stop(self):
        if self.playing:
            self.toggle_playback()