import streamlit as st
from modules.utils import extract_video_id
from youtube_api import YoutubeAPI

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.write("### Youtube Video Stats Viewer 📺")

@st.cache_data
def query_api(channel_description: str) -> list:
    # TODO: Check whether is youtube link or just username before instantiating
    api = YoutubeAPI(video_url=channel_description)
    api.get_uploads_playlist_id()
    api.get_video_ids_from_playlist()
    return api.get_video_stats()

@st.cache_data
def create_plot(data: list):
    df = pd.DataFrame(data)

    df['publishedAt'] = pd.to_datetime(df.publishedAt)
    df['viewCount'] = pd.to_numeric(df.viewCount)
    df['likeCount'] = pd.to_numeric(df.likeCount)
    df['commentCount'] = pd.to_numeric(df.commentCount)

    df.set_index('publishedAt', inplace=True)

    fig, ax = plt.subplots()
    sns.lineplot(data=df, ax=ax)
    plt.xticks(rotation=90)
    plt.show()

    return fig

channel_description = st.text_input("Enter any video url from your chosen channel")
if channel_description:
    stats = query_api(channel_description)
    fig = create_plot(stats)
    st.pyplot(fig)


