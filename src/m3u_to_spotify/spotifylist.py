import os
from .database import Database
from .spotifyrestclient import SpotifyRestClient

class SpotifyList:
    def __init__(self, db_path, user_id, client_id, client_secret, redirect_url) -> None:
        if not os.path.isdir(db_path):
            print('{} is not a directory. Please add DB_PATH in order to continue'.format(db_path))
            exit(1)

        self.user_id = user_id
        self.db = Database(db_path)
        self.client = SpotifyRestClient(user_id=user_id, client_id=client_id, client_secret=client_secret, redirect_url=redirect_url)

    def add_to_list(self, list_name, list_path, mp3):
        track_id = None
        track = self.db.get_track_by(artist=mp3.artist(), title=mp3.title())
        if track:
            track_id = track[0][2]
        else:
            ret = self.client.search(artist=mp3.artist(), title=mp3.title().replace('(Cover)', '').replace('(Symphonic)', ''))
            if ret:
                track_id = ret.get('id')
                self.db.add_track(artist=mp3.artist(), title=mp3.title(), id_spotify=ret.get('id'), url=ret.get('url'))

        if not track_id:
            print('*** {} - {} could not be found'.format(mp3.artist(), mp3.title()))
            return None

        playlist_id = self.create_playlist(list_name, list_path)
        exists = self.db.get_track_in_playlist(id_track=track_id, id_list=playlist_id)
        if not exists and track_id:
            print('Adding track {} - {} to {}'.format(mp3.artist(), mp3.title(), list_name))
            self.client.add_track_to_list(track_id, playlist_id)
            self.db.add_track_to_playlist(track_id, playlist_id)
        else:
            print('Track {} - {} already exists on {}'.format(mp3.artist(), mp3.title(), list_name))

    def create_playlist(self, list_name, list_path):
        playlist = self.db.get_playlist_by(list_name)
        if not playlist:
            ret = self.client.create_list(list_name)
            if not ret:
                print('Could not make request to create list {}'.format(list_name))
                exit(1)

            self.db.add_playlist(list_name, self.user_id, list_path, ret['id'])
            return ret['id']
        else:
            return playlist[0][3]
