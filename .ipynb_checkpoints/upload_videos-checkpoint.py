#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow


# In[ ]:


# Replace with your API key
API_KEY = os.getenv('YOUTUBE_API_KEY')
JSON_SECRETS_PATH = './secrets/oauth_secret.json'

# Replace with the path to the video you want to upload
VIDEO_PATH = 'f:/Jupyter/Manim/venv/media/videos/scene/480p15/DifferentRotations.mp4'

# Scope for YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


# In[ ]:


def get_authenticated_service():
    credentials_file = 'credentials.pickle'

    # Check if credentials already exist
    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(JSON_SECRETS_PATH, SCOPES)
        credentials = flow.run_local_server()

        # Save the credentials for future use
        with open(credentials_file, 'wb') as token:
            pickle.dump(credentials, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(youtube, video_path):
    # Prepare the video resource
    media = MediaFileUpload(video_path)

    # Set the video details
    body = {
        "snippet": {
            "title": "Your Video Title",
            "description": "Your Video Description",
            "tags": ["tag1", "tag2", "tag3"],
            "categoryId": "22"  # Replace with the appropriate category ID for your content
        },
        "status": {
            "privacyStatus": "private"  # Change to "public" if you want to make the video public
        }
    }

    try:
        # Execute the API request to upload the video
        youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
        print("Video uploaded successfully.")
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
        return None


# In[ ]:


if __name__ == "__main__":
    # Initialize the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    # Authenticate and get the authorized service
    # Uncomment the next line if running the script for the first time
    youtube = get_authenticated_service()

    # Upload the video
    upload_video(youtube, VIDEO_PATH)


# In[ ]:




