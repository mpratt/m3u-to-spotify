# M3U to Spotify
Python script used to create spotify lists based on a M3U playlist.
The script uses the id3 information of each file on the list and searches on Spotify
for the song. It creates a playlist on spotify based on the name of the M3U list.
The files must exist on your harddrive in order to work and they must be valid mp3 files.

You need to create an app in spotify, get the client_id, secret_id and redirect_url.
You need your spotify username too and add it into the ini file.

This scripts looks for `~/.config/m3u_to_spotify/m3u_spotify.ini` or you can specify your
own ini file using the `--config` flag.

# Installation
Download the source code, extract the data, go to the folder and run

`pip install -e .`

# Usage
```
m3u-to-spotify /path/to/list.m3u
```
