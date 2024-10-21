import streamlit as st
from modules.utils import extract_video_id
from youtube_api import YoutubeAPI

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go

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
    
    # TODO Add a parameter to chose between seaborn or plotly chart
    # fig, ax = plt.subplots()
    # sns.lineplot(data=df, ax=ax)
    # plt.xticks(rotation=90)
    # plt.show()

    # TODO Attach youtube video title to chart so it shows that on hover
    # fig = px.line(df, x=df.index, y='viewCount')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['viewCount'],
                            mode="lines",
                            name="viewCount"))
    fig.add_trace(go.Scatter(x=df.index, y=df['likeCount'],
                                mode="lines",
                                name="likeCount"))
    fig.add_trace(go.Scatter(x=df.index, y=df['commentCount'],
                            mode="lines",
                            name="commentCount"))

    return fig

channel_description = st.text_input("Enter any video url from your chosen channel")
if channel_description:
    stats = query_api(channel_description)
    fig = create_plot(stats)
    st.plotly_chart(fig)

    # st.pyplot(fig)

    # TODO Deploy app
    #    Requires a public repo

