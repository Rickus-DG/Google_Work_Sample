"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, title):
        self.title = title
        self.videos = {}
    
    def add(self, video):
        self.videos[video.video_id] = video

    def remove(self, video):
        self.videos.pop(video.video_id)
    
    def clear(self):
        self.videos = {}
    
    def title(self):
        return self.title