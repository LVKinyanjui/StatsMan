#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from tqdm import tqdm
from custom import extract_key_from_json


# ## Load Data

# In[2]:


CHANNEL_TITLE = input("Filename (Should match the channel title): ")


# In[3]:


df = pd.read_csv(f"./data/{CHANNEL_TITLE}.csv")


# In[4]:


df.shape


# ## API Call

# In[5]:


import os
from googleapiclient.discovery import build


# In[6]:


API_KEY = os.getenv("YOUTUBE_API_KEY")


# In[7]:


youtube = build("youtube", "v3", developerKey=API_KEY)


# ### Video Stats

# In[8]:


def get_stats(VIDEO_ID):
    response = youtube.videos().list(
        part="statistics",
        id=VIDEO_ID
    ).execute()
    return response


# In[9]:


video_ids = df.id


# In[10]:


video_stats = []
for video_id in tqdm(video_ids):
    video_stats.append(get_stats(video_id))


# In[11]:


stats = pd.DataFrame(extract_key_from_json(video_stats, 'statistics'))
stats.head()


# ## Merge and Name Dataframe

# In[12]:


stats_ = pd.concat([df, stats], axis=1)


# In[13]:


VIDEO_ID = df.id[0]


# In[14]:


video_response = youtube.videos().list(
    part="snippet",
    id=VIDEO_ID
).execute()


# In[15]:


CHANNEL_TITLE = extract_key_from_json(video_response, 'channelTitle')[0]
CHANNEL_TITLE


# ## Save

# In[16]:


stats_.to_csv(f"./data/{CHANNEL_TITLE}.csv", index=False)


# In[ ]:




