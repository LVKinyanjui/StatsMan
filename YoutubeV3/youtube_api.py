from googleapiclient.discovery import build
import asyncio
import os


from modules.exceptions import NoItemsReturned
from modules.utils import extract_video_id
from modules.async_functions import (
    aget_video_ids_from_playlist,
    aget_video_stats
)

class YoutubeAPI:
    
    def __init__(self, channel_username: str = None, video_url: str = None):
        api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=api_key)
        
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
        request = self.youtube.videos().list(
            part="snippet",
            id=self.video_id
        )
        response = request.execute()

        try:
            return response['items'][0]['snippet']['channelId']
        except KeyError:
            raise NoItemsReturned(f"No video found for video ID: {self.video_id}")


    def get_uploads_playlist_id(self):
        request = self.youtube.channels().list(
            part="contentDetails",
            id=self.channel_id
        )
        response = request.execute()

        if response["pageInfo"]["totalResults"] == 0:
            raise NoItemsReturned(f"No results returned from endpoint: {request.methodId}")
        
        self.uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return self.uploads_playlist_id
    
    def get_video_ids_from_playlist(self, max_results=50) -> list:
        video_ids = []
        next_page_token = None

        # TODO: Perfom each request asynchronously to reduce wait times
        while True:
            request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=self.uploads_playlist_id,
                maxResults=max_results,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_ids.append(video_id)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        self.video_ids = video_ids
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