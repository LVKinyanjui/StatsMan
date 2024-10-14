#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tweet_generator import TweetGenerator
from twitter_api import TwitterAPI


# In[2]:


from generation.gemini import Gemini


# ### Post Topic
# The generation of ideas should be done by agents. The aim is to use the autogen framework to generate and criticize ideas on their merit before writing anything about them.

# In[3]:


user_topic = """
    You are to generate a story on how clumsily interpreting p-values 
    may have led to ridiculous outcomes when doing statistical research.
"""


# In[4]:


prompt = f"""
    You are to imagine yourself as an avid twitter (or X user)
    You create interesting and captivating tweets for your audience
    You throw in some humour, irony and sarcasm where appropriate

    You begin the first 100 or so words of your tweet with a HOOK
    something that teases the audience with what you wish to share
    Then you tell your story to reflect your HOOK or initial introduction

    DO NOT use the words HOOK or STORY in your actual response
    JUst write out the story
    
    You are to apply the aforementioned instructions to the following topic

    {user_topic}
"""


# In[5]:


generator = TweetGenerator(model_type='gemini')
tweets = generator.generate_tweets(prompt)
tweets


# In[6]:


main_tweet = tweets[0]
replies = tweets[1:]


# In[7]:


twitterAPI = TwitterAPI()
twitterAPI.tweet_thread(main_tweet, replies)


# In[ ]:




