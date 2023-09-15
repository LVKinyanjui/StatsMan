# %% [markdown]
# In this notebook we will be searching for data on a given topic to find summary statistics about that topic. The hope is to be able to do large scale data collection for analysis of a given social topic such as economic developments.

# %%
import os
import pandas as pd
from datetime import datetime
from pyautogui import prompt
from googleapiclient.discovery import build

# %%
API_KEY = os.getenv("YOUTUBE_API_KEY")

# %%
youtube = build('youtube', 'v3', developerKey=API_KEY)

# %%
# search_query = input("Enter Search Terms:")
search_query = prompt(text="Enter your desired search term", title="Youtube Search", default="recession")
max_results = int(prompt(text="Enter how many results to return", title="YouTube Search", default=100))

# %%
# Date in a format usable by Youtube API
start_date = datetime(2022, 2, 20).isoformat() + 'Z'  
end_date = datetime(2023, 12, 31).isoformat() + 'Z'  


# %%
# Call the search.list method to retrieve search results, including publish date
search_response = youtube.search().list(
    q=search_query,
    type='video',
    part='id,snippet',
    maxResults=10,
    order='date',  # Sort by date (most recent first)
    publishedAfter=start_date,  # Filter by publish date after the start date
).execute()


# %%
# Extract and print the video titles, IDs, and publish dates
contents = []
for search_result in search_response.get('items', []):
    video_id = search_result['id']['videoId']
    video_title = search_result['snippet']['title']
    publish_date = search_result['snippet']['publishedAt']
    
    contents.append(
        {
            "publish_date": publish_date,
            "video_id": video_id,
            "video_title": video_title
        }
    )

    print(f'Video Title: {video_title}, Video ID: {video_id}, Publish Date: {publish_date}')
    

# %%
data = pd.DataFrame(contents)
data.head()

# %%
data.to_csv(f"data/search {search_query}.csv")

# %%



