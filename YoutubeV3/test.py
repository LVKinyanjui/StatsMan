import requests
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")

# Function to get channel ID from a video ID
def get_channel_id_by_video_id(video_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet"
        f"&id={video_id}"
        f"&key={API_KEY}"
    )
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['snippet']['channelId']
        else:
            print(f"No video found for video ID: {video_id}")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to get uploads playlist ID from channel ID
def get_uploads_playlist_id(channel_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/channels"
        f"?part=contentDetails"
        f"&id={channel_id}"
        f"&key={API_KEY}"
    )
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            return uploads_playlist_id
        else:
            print(f"No channel found for channel ID: {channel_id}")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

if __name__ == "__main__":
    # Test the functions
    video_id = 'YjRP7USZBqI'  # Replace with your video ID
    channel_id = get_channel_id_by_video_id(video_id)
    
    if channel_id:
        print(f"Channel ID: {channel_id}")
        
        uploads_playlist_id = get_uploads_playlist_id(channel_id)
        if uploads_playlist_id:
            print(f"Uploads Playlist ID: {uploads_playlist_id}")
