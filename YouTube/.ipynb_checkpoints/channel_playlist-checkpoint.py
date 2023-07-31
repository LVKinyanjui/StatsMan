#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
from googleapiclient.discovery import build


# In[2]:


from custom import extract_key_from_json


# In[3]:


API_KEY = os.getenv("YOUTUBE_API_KEY")
API_KEY


# In[4]:


if API_KEY is not None:
    youtube = build("youtube", "v3", developerKey=API_KEY)


# ## From video id to channel id, name

# In[5]:


VIDEO_ID = input("Video id: ")


# In[6]:


video_response = youtube.videos().list(
    part="snippet",
    id=VIDEO_ID
).execute()


# In[7]:


CHANNEL_ID = extract_key_from_json(video_response, 'channelId')[0]


# In[8]:


CHANNEL_TITLE =  extract_key_from_json(video_response, 'channelTitle')[0]


# ## From channel id to playlist id

# In[9]:


# Step 1: Get Uploads Playlist ID
youtube = build('youtube', 'v3', developerKey=API_KEY)
channel_response = youtube.channels().list(
    part='contentDetails',
    id=CHANNEL_ID
).execute()

uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


# ## From playlist id to video titles

# In[10]:


# Step 2: Get Video Titles from the Playlist
video_data = []
next_page_token = None

while True:
    playlist_response = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=next_page_token
    ).execute()

    for item in playlist_response['items']:
        video_title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        video_data.append({'title': video_title, 'id': video_id})

    next_page_token = playlist_response.get('nextPageToken')
    if not next_page_token:
        break


# ## Save

# In[11]:


df = pd.DataFrame(video_data)
df.to_csv(f"./data/{CHANNEL_TITLE}.csv", index=False)


# In[ ]:




