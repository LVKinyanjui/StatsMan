#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from googleapiclient.discovery import build
from custom import extract_key_from_json, clean_string

import pandas as pd


# ## Credentials

# In[2]:


VIDEO_ID = input("Enter any video ID from the channel of interest: ")
API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_USERNAME = "@RockstarAcademy"


# In[3]:


# Create a YouTube API client
# MUST be initialized
youtube = build("youtube", "v3", developerKey=API_KEY)


# ## Functions

# In[4]:


def get_commentThreads (video_id, max_results=100):
    
    #Looping over pages
    comments = []
    next_page_token = None
    
    while 1:
        res = youtube.commentThreads().list(part = 'snippet', 
                                            videoId = video_id,
                                            pageToken = next_page_token,
                                            maxResults = max_results
                                           ).execute()
        comments += res['items']
        next_page_token = res.get('nextPageToken')
        
        # If token is none then we have reached the end so break
        if  next_page_token == None:
            break
            
    return comments


# In[5]:


def get_video_details(video_id):
    response = youtube.videos().list(
        part="snippet, statistics", 
        id=video_id
    ).execute()

    video_title = clean_string(extract_key_from_json(response, "title")[0])

    comment_count = int(extract_key_from_json(response, "commentCount")[0])
    
    return video_title, comment_count


# In[6]:


def save(video_title, comments):
    path = "./data/" + video_title + ".csv"

    df = pd.DataFrame()
    df['text'] = comments
    df.to_csv(path, index=False, encoding="utf-8")


# In[8]:


if __name__ == "__main__":
    video_title, total_comments = get_video_details(VIDEO_ID)
    response = get_commentThreads(VIDEO_ID, max_results=total_comments)
    comments = extract_key_from_json(response, 'textOriginal')
    save(video_title, comments)


# In[ ]:




