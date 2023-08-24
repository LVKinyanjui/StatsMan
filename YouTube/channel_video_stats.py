#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from tqdm import tqdm
from custom import extract_key_from_json


# ## Load Data

# In[1]:


CHANNEL_TITLE = input("Filename (Should match the channel title): ")


# In[4]:


df = pd.read_csv(f"./data/{CHANNEL_TITLE}.csv")


# In[5]:


df.shape


# ## API Call

# In[6]:


import os
from googleapiclient.discovery import build


# In[7]:


API_KEY = os.getenv("YOUTUBE_API_KEY")


# In[8]:


youtube = build("youtube", "v3", developerKey=API_KEY)


# ### Video Stats

# In[9]:


def get_stats(VIDEO_ID):
    response = youtube.videos().list(
        part="statistics, contentDetails",
        id=VIDEO_ID
    ).execute()
    return response


# In[10]:


video_ids = df.id


# In[11]:


video_stats = []
for video_id in tqdm(video_ids):
    video_stats.append(get_stats(video_id))


# In[ ]:


extract_key_from_json(video_stats, 'duration')


# In[22]:


stats = pd.DataFrame(extract_key_from_json(video_stats, 'statistics'))
stats['duration'] = extract_key_from_json(video_stats, 'duration')

stats.head()


# ## Merge and Name Dataframe

# In[23]:


stats_ = pd.concat([df, stats], axis=1)


# In[24]:


VIDEO_ID = df.id[0]


# In[25]:


video_response = youtube.videos().list(
    part="snippet",
    id=VIDEO_ID
).execute()


# In[26]:


CHANNEL_TITLE = extract_key_from_json(video_response, 'channelTitle')[0]
CHANNEL_TITLE


# ## Save

# In[27]:


stats_.to_csv(f"./data/{CHANNEL_TITLE}.csv", index=False)


# In[ ]:




