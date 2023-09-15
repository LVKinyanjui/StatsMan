# %%
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# %%
import re
import time
import sys

# %%
CHANNEL_TITLE = input("Filename (Should match the channel title): ")
topic = input("topic to get statistics of: ")

# %% [markdown]
# ## Preprocessing

# %%
try:
    df = pd.read_csv(f"./data/{CHANNEL_TITLE}.csv")
except:
    print(f"File with {CHANNEL_TITLE} has not been found")
    time.sleep(5)
    sys.exit()

# %%
try:
    df.viewCount
    df.likeCount
except AttributeError:
    print("viewCount and likeCount columns not found in dataframe")
    time.sleep(5)
    sys.exit()

# %%
# Filtering by serach time
df_ = df[df.title.str.contains(topic)]

# %%
# Setting publish date as inde
df.date_published = pd.to_datetime(df.date_published)

df.set_index('date_published', inplace=True)
df.head(2)

# %% [markdown]
# ## Plots (Overall)

# %%
plt.figure(figsize=(15, 6))
sns.lineplot(df)
plt.title("View Count")
plt.xticks(rotation=90)
plt.show()

# %%
np.median(df.viewCount)

# %%
if df_.shape[0] != 0:
    # Most viewed video
    most_viewed= list(df_.sort_values(by='viewCount', ascending=False).title)[0]
    print(f"For Topic: {topic} \n\n Most Viewed: {most_viewed}")
else:
    most_viewed= list(df.sort_values(by='viewCount', ascending=False).title)[0]
    print(f"Pattern selected dataframe empty \n Diaplaying full dataframe stats \n\n Most Viewed: {most_viewed}")

# %% [markdown]
# ## Duration
# The documentation tells us as much about `contentDetails.duration`:
# > The length of the video. The property value is an ISO 8601 duration. For example, for a video that is at least one minute long and less than one hour long, the duration is in the format PT#M#S, in which the letters PT indicate that the value specifies a period of time, and the letters M and S refer to length in minutes and seconds, respectively. The # characters preceding the M and S letters are both integers that specify the number of minutes (or seconds) of the video. For example, a value of PT15M33S indicates that the video is 15 minutes and 33 seconds long.

# %%
time_length = '17M'
df[df.duration.str.contains(time_length)]

# %%



