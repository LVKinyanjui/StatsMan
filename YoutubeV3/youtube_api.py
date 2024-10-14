from googleapiclient.discovery import build
import os

class YoutubeAPI:
    
    def __init__(self, channel_username: str):
        api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.username = channel_username

    def get_channel_id_by_username(self):
        request = self.youtube.channels().list(
            part="id",
            forUsername=self.username
        )
        response = request.execute()

        try:
            return response['items'][0]['id']
        except KeyError:
            raise SystemExit(f"No channel found for username: {self.username} \nTry Another")

if __name__ == "__main__":
    username = "GoogleDevelopers"
    youtube = YoutubeAPI(username)
    channel_id = youtube.get_channel_id_by_username()
    print(channel_id)