from googleapiclient.discovery import build
import asyncio
import requests
import os

from modules.exceptions import NoItemsReturned
from modules.utils import extract_video_id
from modules.async_functions import aget_video_stats
from modules.async_functions2 import aget_video_ids_from_playlist

class YoutubeAPI:
    
    def __init__(self, channel_username: str = None, video_url: str = None):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        # self.youtube = build("youtube", "v3", developerKey=self.api_key)
        
        self.video_id = self.video_id = extract_video_id(video_url)

        if video_url is not None:
            self.channel_id = self._get_channel_id_by_video_id()

        if channel_username is not None:
            self.username = channel_username
            self.channel_id = self._get_channel_id_by_username()     # Trivial and necessary for all subsequent operations

        # Attributes initially set to none as changes to class structure are expectes
        # and may not be necessary to call their methods in the constructor
        # as some may be optional and others long running
        self.uploads_playlist_id = None
        self.video_ids = None
        self.video_stats = None

    def _get_channel_id_by_username(self):
        request = self.youtube.channels().list(
            part="id",
            forUsername=self.username
        )
        response = request.execute()

        try:
            return response['items'][0]['id']
        except KeyError:
            raise NoItemsReturned(f"No channel found for username: {self.username} \nTry Another")
        
    def _get_channel_id_by_video_id(self):
        url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?part=snippet"
            f"&id={self.video_id}"
            f"&key={self.api_key}"
        )
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]['snippet']['channelId']
            else:
                print(f"No video found for video ID: {self.video_id}")
                return None
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    def get_uploads_playlist_id(self):
        url = (
            f"https://www.googleapis.com/youtube/v3/channels"
            f"?part=contentDetails"
            f"&id={self.channel_id}"
            f"&key={self.api_key}"
        )
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                self.uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                return self.uploads_playlist_id
            else:
                print(f"No channel found for channel ID: {self.channel_id}")
                return None
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    
    def get_video_ids_from_playlist(self, max_results=50) -> list:
        # video_ids = []
        # next_page_token = None

        # # TODO: Perfom each request asynchronously to reduce wait times
        # while True:
        #     request = self.youtube.playlistItems().list(
        #         part="snippet",
        #         playlistId=self.uploads_playlist_id,
        #         maxResults=max_results,
        #         pageToken=next_page_token
        #     )
        #     response = request.execute()

        #     for item in response['items']:
        #         video_id = item['snippet']['resourceId']['videoId']
        #         video_ids.append(video_id)

        #     next_page_token = response.get('nextPageToken')
        #     if not next_page_token:
        #         break

        # self.video_ids = video_ids
        self.video_ids = asyncio.run(aget_video_ids_from_playlist(self.uploads_playlist_id))
        return self.video_ids

    def get_video_stats(self):
        # video_stats = []
        # for i in range(0, len(self.video_ids), 50):  # YouTube API accepts up to 50 video IDs per request
        #     request = self.youtube.videos().list(
        #         part="statistics,contentDetails,snippet",
        #         id=','.join(self.video_ids[i:i+50])
        #     )
        #     response = request.execute()

        #     for item in response['items']:
        #         stats = {
        #             'videoId': item['id'],
        #             'viewCount': item['statistics'].get('viewCount', 0),
        #             'likeCount': item['statistics'].get('likeCount', 0),
        #             'commentCount': item['statistics'].get('commentCount', 0),
        #             'duration': item['contentDetails']['duration'],
        #             'videoTitle': item['snippet']['title'],
        #             'publishedAt': item['snippet']['publishedAt'],
        #         }
        #         video_stats.append(stats)

        video_stats = asyncio.run(aget_video_stats(self.video_ids))

        self.video_stats = video_stats
        return self.video_stats


if __name__ == "__main__":
    # Execute in order
    api = YoutubeAPI(video_url="https://www.youtube.com/watch?v=vum0-y47cvw")
    api.get_uploads_playlist_id()
    api.get_video_ids_from_playlist()
    api.get_video_stats()