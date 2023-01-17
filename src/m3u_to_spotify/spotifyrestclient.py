import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyRestClient:
    def __init__(self, user_id, client_id, client_secret, redirect_url):
        self.user_id = user_id
        self.redirect_url = redirect_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.spotify = self.get_client()

    def get_client(self):
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-private, playlist-modify-public",
                redirect_uri=self.redirect_url,
                client_id=self.client_id,
                client_secret=self.client_secret,
        ))

    def search(self, artist, title):
        try:
            result = self.spotify.search(q='{} artist:{}'.format(title, artist), type='track', market='US', limit=5)
            return {
                    'id': result['tracks']['items'][0]['id'],
                    'uri': result['tracks']['items'][0]['uri'],
                    'url': result['tracks']['items'][0]['external_urls']['spotify']
            }
        except IndexError:
            return None

    def add_track_to_list(self, track_id, list_id):
        return self.spotify.playlist_add_items(list_id, [track_id])

    def create_list(self, list_name):
        return self.spotify.user_playlist_create(self.user_id, list_name)
