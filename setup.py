import os
from setuptools import setup, find_packages

DEPENDENCIES = ( 'eyed3', 'spotipy' )

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'm3u-to-spotify',
    version = '0.1.0',
    author = "Michael Pratt",
    author_email = "author@michaelpratt.dev",
    description = ( "Create spotify playlists based on m3u lists" ),
    license = "MIT",
    keywords = "",
    include_package_data=True,
    url = "",
    packages = find_packages(),
    package_dir = { '' : 'src' },
    long_description = read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=DEPENDENCIES,
    entry_points = {
        'console_scripts': [ 'm3u-to-spotify = m3u_to_spotify.cli:start' ],
    },
)
