"""A video player class."""

from src.video_playlist import Playlist
from .video_library import VideoLibrary
import random
import re
from src import video_library


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._video_playing = None
        self._is_paused = False
        self._playlists = {}
        self._flagged = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        
        print("Here's a list of all available videos:")
        videos = self._video_library.get_all_videos()
        video_details = []
        for video in videos:
            if self._flagged.get(video.video_id) != None:
                video_details.append(video.details() + " - FLAGGED (reason: " + self._flagged[video.video_id] + ")")
            else:
                video_details.append(video.details())
        video_details.sort()
        for video_detail in video_details:
            print(video_detail)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
    
        old_video = self._video_playing
        self._video_playing = None
        for video in self._video_library.get_all_videos():
            if video_id == video.video_id:
                self._video_playing = video

        if self._video_playing != None and self._flagged.get(video_id) != None:
            print("Cannot play video: Video is currently flagged (reason: " + self._flagged[self._video_playing.video_id] + ")")
            return
        
        if old_video != None and self._video_playing != None:
            print("Stopping video: " + old_video.title)
            self._is_paused = False
        if self._video_playing == None:
            print("Cannot play video: Video does not exist")
        else:
            self._is_paused = False
            print("Playing video: " + self._video_playing.title)

    def stop_video(self):
        """Stops the current video."""

        if self._video_playing != None:
            print("Stopping video: " + self._video_playing.title)
            self._video_playing = None
            self._is_paused = False
        else:
            print("Cannot stop video: No video is currently playing")        

    def play_random_video(self):
        """Plays a random video from the video library."""

        videos = self._video_library.get_all_videos()
        videos_available = []
        for video in videos:
            if self._flagged.get(video.video_id) == None:
                videos_available.append(video)
        if videos_available == None or len(videos_available) == 0:
            print("No videos available")
            return
        random_index = random.randrange(len(videos_available))
        video_id = videos_available[random_index].video_id
        self.play_video(video_id)


    def pause_video(self):
        """Pauses the current video."""

        if self._is_paused:
            print("Video already paused: " + self._video_playing.title)
        elif self._video_playing == None:
            print("Cannot pause video: No video is currently playing")
        else:
            print("Pausing video: " + self._video_playing.title)
            self._is_paused = True

    def continue_video(self):
        """Resumes playing the current video."""

        if self._is_paused:
            print("Continuing video: " + self._video_playing.title)
            self._is_paused = False 
        elif self._video_playing == None:
            print("Cannot continue video: No video is currently playing")
        elif not self._is_paused and self._video_playing != None:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""

        message = ""
        if self._video_playing != None:
            message = "Currently playing: " + self._video_playing.details()
            if self._is_paused:
                message += " - PAUSED"
        else:
            message = "No video is currently playing"

        print(message)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        mixed_caps_name = playlist_name
        playlist_name = playlist_name.lower()
        if self._playlists.get(playlist_name) is not None:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlists[playlist_name] = Playlist(mixed_caps_name)
            print("Successfully created new playlist: " + mixed_caps_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        mixed_caps_name = playlist_name
        playlist_name = playlist_name.lower()
        video = self._video_library.get_video(video_id)
        if self._flagged.get(video_id) != None:
            print("Cannot add video to my_playlist: Video is currently flagged (reason: " + self._flagged[video_id] + ")")
            return

        if self._playlists.get(playlist_name) is None:
            print("Cannot add video to " + mixed_caps_name + ": Playlist does not exist")
        elif video == None:
            print("Cannot add video to " + mixed_caps_name + ": Video does not exist")
        elif self._playlists[playlist_name].videos.get(video_id) is not None:
            print("Cannot add video to " + mixed_caps_name + ": Video already added")
        else:
            self._playlists[playlist_name].add(video)
            print("Added video to " + mixed_caps_name + ": " + video.title)

    def show_all_playlists(self):
        """Display all playlists."""

        if self._playlists == {}:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for playlist in sorted(self._playlists):
                print(self._playlists[playlist].title)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlists.get(playlist_name.lower()) is None:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")
        else:
            print("Showing playlist: " + playlist_name)
            videos = self._playlists[playlist_name.lower()].videos
            if videos == {}:
                print("No videos here yet")
            else:
                for videoID in videos:
                    if self._flagged.get(videoID) != None:
                        print(videos[videoID].details() + " - FLAGGED (reason: " + self._flagged[videoID] + ")")
                    else:
                        print(videos[videoID].details())

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        if self._playlists.get(playlist_name.lower()) == None:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")
            return
        playlist = self._playlists[playlist_name.lower()]
        
        for video_in_playlist in playlist.videos:
            if video_id == playlist.videos[video_in_playlist].video_id:
                video = self._video_library.get_video(video_id)
                playlist.remove(video)
                print("Removed video from " + playlist_name + ": " + video.title)
                return

        for video_in_library in self._video_library.get_all_videos():
            if video_id == video_in_library.video_id:
                print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
                return
        print("Cannot remove video from " + playlist_name + ": Video does not exist")
        

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlists.get(playlist_name.lower()) == None:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")
            return

        playlist = self._playlists[playlist_name.lower()]
        playlist.clear()
        print("Successfully removed all videos from " + playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self._playlists.get(playlist_name.lower()) == None:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")
            return
        self._playlists.pop(playlist_name.lower())
        print("Deleted playlist: " + playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        hits = []
        for video in self._video_library.get_all_videos():
            if search_term in video.details() and self._flagged.get(video.video_id) == None:
                hits.append(video.details())
        if len(hits) == 0:
            print("No search results for " + search_term)
            return
        hits.sort()
        print("Here are the results for " + search_term + ":")
        index = 1
        for hit in hits:
            print(str(index) + ") " + hit)
            index += 1
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        choice = input()
        if not choice.isdigit():
            return
        choice = int(choice)
        if choice < 1 or choice > len(hits):
            return
        
        regex = re.compile(r'\(.*\)')
        id_match = regex.search(hits[choice-1])
        id = id_match.group().strip("()")
        self.play_video(id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        hits = []
        for video in self._video_library.get_all_videos():
            if video_tag in ''.join(video.tags) and self._flagged.get(video.video_id) == None:
                hits.append(video.details())
        if len(hits) == 0:
            print("No search results for " + video_tag)
            return
        hits.sort()
        print("Here are the results for " + video_tag + ":")
        index = 1
        for hit in hits:
            print(str(index) + ") " + hit)
            index += 1
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        choice = input()
        if not choice.isdigit():
            return
        choice = int(choice)
        if choice < 1 or choice > len(hits):
            return
        regex = re.compile(r'\(.*\)')
        id_match = regex.search(hits[choice-1])
        id = id_match.group().strip("()")
        self.play_video(id)
        

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot flag video: Video does not exist")
            return

        if self._flagged.get(video_id) != None:
            print("Cannot flag video: Video is already flagged")
            return
        
        if self._video_playing != None and video_id == self._video_playing.video_id :
            self.stop_video()
        
        if flag_reason == "":
            flag_reason = "Not supplied"
        self._flagged[video_id] = flag_reason
        print("Successfully flagged video: " + video.title + " (reason: " + flag_reason + ")")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot remove flag from video: Video does not exist")
            return

        if self._flagged.get(video_id) == None:
            print("Cannot remove flag from video: Video is not flagged")
            return
            
        self._flagged.pop(video_id)
        print("Successfully removed flag from video: " + video.title)