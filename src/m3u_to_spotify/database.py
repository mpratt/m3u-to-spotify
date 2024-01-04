import sqlite3

class Database:
    def __init__(self, db_path):
        self.database_location = '{}/spotify.sqlite'.format(db_path)
        self.db = sqlite3.connect(self.database_location)
        self.create_tables()

    def create_tables(self):
        self.db.execute('CREATE TABLE IF NOT EXISTS playlists (playlist text, user_id text, m3u text, id_spotify text)')
        self.db.execute('CREATE TABLE IF NOT EXISTS playlist_tracks (id_track text, id_list text)')
        self.db.execute('CREATE TABLE IF NOT EXISTS tracks (title text, artist text, id_spotify text, url text)')

    def add_track(self, title, artist, id_spotify, url):
        self.db.execute('INSERT INTO tracks (title, artist, id_spotify, url) VALUES (?, ?, ?, ?)', (title, artist, id_spotify, url))
        self.db.commit()

    def add_playlist(self, playlist, user_id, m3u, id_spotify):
        self.db.execute('INSERT INTO playlists (playlist, user_id, m3u, id_spotify) VALUES (?, ?, ?, ?)', (playlist, user_id, m3u, id_spotify))
        self.db.commit()

    def add_track_to_playlist(self, id_track, id_list):
        self.db.execute('INSERT INTO playlist_tracks (id_track, id_list) VALUES (?, ?)', (id_track, id_list))
        self.db.commit()

    def truncate_playlist(self, id_list):
        self.db.execute('DELETE FROM playlist_tracks WHERE id_list = ?', (id_list, ))
        self.db.commit()

    def get_track_in_playlist(self, id_track, id_list):
        rows = self.db.execute('SELECT * FROM playlist_tracks WHERE id_track = ? AND id_list = ?', (id_track, id_list)).fetchall()
        return rows if len(rows) > 0 else None

    def get_track_by(self, title, artist):
        rows = self.db.execute('SELECT title, artist, id_spotify, url FROM tracks WHERE title = ? AND artist = ?', (title, artist)).fetchall()
        return rows if len(rows) > 0 else None

    def get_playlist_by(self, playlist):
        rows = self.db.execute('SELECT playlist, user_id, m3u, id_spotify FROM playlists WHERE playlist = ?', (playlist, )).fetchall()
        return rows if len(rows) > 0 else None
