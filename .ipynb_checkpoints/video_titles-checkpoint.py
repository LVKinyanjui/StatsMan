#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import csv
from googleapiclient.discovery import build


# ## Functions

# In[ ]:


def extract_key_from_json(json_data, target_key):
    result = []

    def search_nested(json_obj, key):
        if isinstance(json_obj, dict):
            for k, v in json_obj.items():
                if k == key:
                    result.append(v)
                elif isinstance(v, (dict, list)):
                    search_nested(v, key)
        elif isinstance(json_obj, list):
            for item in json_obj:
                search_nested(item, key)

    search_nested(json_data, target_key)
    return result


# ## API Call

# In[ ]:


VIDEO_ID = input("Enter any video ID from the channel of interest: ")
API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_USERNAME = "@RockstarAcademy"


# In[ ]:


# Create a YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)


# In[28]:


# Get the channel ID using a random video ID from the channel
channels_response = youtube.videos().list(
    part="snippet",
    id=VIDEO_ID
).execute()

channel_id = extract_key_from_json(channels_response, 'channelId')


# In[51]:


# Request the playlist ID of the channel's uploaded videos
channels_response = youtube.channels().list(
    part="snippet,contentDetails",
    id=channel_id
).execute()

playlist_id = extract_key_from_json(channels_response, 'uploads')
channel_username = extract_key_from_json(channels_response, 'customUrl')[0]


# In[31]:


# Retrieve the video titles from the playlist
videos = []
next_page_token = None

while True:
    playlist_items_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50,
        pageToken=next_page_token
    ).execute()

    for item in playlist_items_response["items"]:
        title = item["snippet"]["title"]
        videos.append(title)

    next_page_token = playlist_items_response.get("nextPageToken")

    if not next_page_token:
        break


# In[52]:


filename = f"./data/{channel_username}.csv"
with open(filename, "w", encoding='utf-8') as file:
    file.write('text' + '\n')
    for video in videos:
        file.write(video + "\n")


# In[ ]:




