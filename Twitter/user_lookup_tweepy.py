import tweepy
import os

client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

reponse = client.get_user(username='lii_karis', user_fields=["created_at"])
print(response.data)

