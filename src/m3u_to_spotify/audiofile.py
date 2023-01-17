from dataclasses import dataclass
from eyed3 import core

@dataclass
class AudioFile:
    media: core.AudioFile

    def artist(self) -> str:
        return self.media.tag.artist

    def title(self) -> str:
        return self.media.tag.title

    def album(self) -> str|None:
        try:
            return self.media.tag.album
        except:
            return None

    def year(self):
        try:
            return self.media.tag.getBestDate().year
        except:
            return 0
