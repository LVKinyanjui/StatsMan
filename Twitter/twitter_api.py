import tweepy
import os
from dotenv import load_dotenv

class TwitterAPI:

    def __init__(self):

        if load_dotenv:
            (consumer_key, ) = os.getenv('TWITTER_CONSUMER_KEY'),
            self.consumer_key = consumer_key
            (consumer_secret, ) = os.getenv('TWITTER_CONSUMER_KEY_SECRET'),
            self.consumer_secret = consumer_secret
            (access_token, ) = os.getenv('TWITTER_ACCESS_TOKEN'),
            self.access_token = access_token
            (access_secret, ) = os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            self.access_secret = access_secret

            self.client = self.twitConnection()
        else:
            raise Exception("Environmental variables not set in .env file")

        # self.client = tweepy.Client(
        #     consumer_key = consumer_key, consumer_secret=consumer_secret,
        #     access_token=access_token, access_token_secret=access_secret)

    def twitConnection(self):
        client = tweepy.Client(
            consumer_key = self.consumer_key, consumer_secret=self.consumer_secret,
            access_token=self.access_token, access_token_secret=self.access_secret)

        return client

    def tweet_thread(self, first_tweet_text, replies):
        last_tweet_id = ''
        first_tweet = self.client.create_tweet(text=first_tweet_text)
        last_tweet_id = first_tweet.data['id']
        for reply in replies:
            reply_tweet = self.client.create_tweet(text=reply, in_reply_to_tweet_id=last_tweet_id)
            last_tweet_id = reply_tweet.data['id']
