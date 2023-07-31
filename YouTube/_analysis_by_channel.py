#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from tqdm import tqdm
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


import re
import time
import sys


# In[3]:


CHANNEL_TITLE = input("Filename (Should match the channel title): ")
pattern = input("Pattern to get statistics of")


# In[4]:


try:
    df = pd.read_csv(f"./data/{CHANNEL_TITLE}.csv")
except:
    print(f"File with {CHANNEL_TITLE} has not been found")
    time.sleep(5)
    sys.exit()


# In[5]:


try:
    df.viewCount
    df.likeCount
except AttributeError:
    print("viewCount and likeCount columns not found in dataframe")
    time.sleep(5)
    sys.exit()


# In[6]:


# pattern = r'ai'


# In[7]:


df_ = df[df.title.str.contains(pattern)]


# In[8]:


df_.head(2)


# ## Plots

# ### Most Viewed

# In[9]:


sns.scatterplot(data=df_, y='viewCount', x='id')
plt.title("View Count")
plt.xticks(rotation=90)
plt.show()


# In[10]:


np.mean(df_.viewCount)


# In[11]:


# Most viewed video
most_viewed= list(df_.sort_values(by='viewCount', ascending=False).title)[0]
most_viewed


# ## Like Count

# In[12]:


sns.scatterplot(data=df_, y='likeCount', x='id', color='green')
plt.title("likeCount")
plt.xticks(rotation=90)
plt.show()


# In[ ]:




