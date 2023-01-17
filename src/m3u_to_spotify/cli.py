import os
import pathlib
import eyed3
from configparser import ConfigParser
from argparse import ArgumentParser
from .audiofile import AudioFile
from .spotifylist import SpotifyList

def start():
    parser = ArgumentParser(description = __name__)
    parser.add_argument( 'm3u_file', help = 'The path to the m3u playlist')
    parser.add_argument( '--config', help = 'Path to Configuration file')
    args = parser.parse_args()
    config_file = args.config
    m3u_file = os.path.abspath(args.m3u_file)

    if not os.path.isfile(m3u_file):
        parser.print_help()
        print("\nERROR: {} is not a m3u file.".format(m3u_file))
        exit(1)

    dot_dir = os.path.expanduser('~/.config/m3u_to_spotify')
    pathlib.Path(dot_dir).mkdir(parents=True, exist_ok=True)
    if not config_file:
        config_file = '{}/m3u_spotify.ini'.format(dot_dir)

    if not os.path.isfile(config_file):
        parser.print_help()
        print("\nERROR: {} is not a valid config file.".format(config_file))
        exit(1)

    config = ConfigParser()
    config.read(config_file)
    if not os.path.isdir(config['M3U_TO_SPOTIFY']['DB_PATH']):
        config['M3U_TO_SPOTIFY']['DB_PATH'] = dot_dir

    if not os.path.isdir(config['M3U_TO_SPOTIFY']['DB_PATH']):
        dotfile = os.path.expanduser('~/.config/m3u_to_spotify')
        pathlib.Path(dotfile).mkdir(parents=True, exist_ok=True)
        config['M3U_TO_SPOTIFY']['DB_PATH'] = dotfile

    playlist = open(m3u_file, 'r')
    playlist_name = os.path.basename(m3u_file).replace('.m3u', '').capitalize()
    spotify = SpotifyList(
            db_path=config['M3U_TO_SPOTIFY']['DB_PATH'],
            user_id=config['M3U_TO_SPOTIFY']['USER_ID'],
            client_id=config['M3U_TO_SPOTIFY']['CLIENT_ID'],
            client_secret=config['M3U_TO_SPOTIFY']['CLIENT_SECRET'],
            redirect_url=config['M3U_TO_SPOTIFY']['REDIRECT_URL']
    )

    print('Creating/updating list {} on {}'.format(playlist_name, m3u_file))
    while (line := playlist.readline().rstrip()):
        if os.path.isfile(line):
            try:
                spotify.add_to_list(playlist_name, m3u_file, AudioFile(media = eyed3.load(line.strip())))
            except:
                pass

if __name__ == "__main__":
    start()
