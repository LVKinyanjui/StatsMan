import tweepy
import json, random

tweet_text = "BanRutoAtUNGA79" * random.randint(2, 5)

with open("secrets/secrets.jsonl", encoding="utf-8") as fp:
    accounts = [json.loads(line) for line in fp]

# Pick an account
# TODO Name the accounts in jsonl
secrets = [account for account in accounts 
           if account["USERNAME"] == "HadrianPasha"][0]

client = tweepy.Client(
    consumer_key=secrets["TWITTER_CONSUMER_KEY"],
    consumer_secret=secrets["TWITTER_CONSUMER_KEY_SECRET"],
    access_token=secrets["TWITTER_ACCESS_TOKEN"],
    access_token_secret=secrets["TWITTER_ACCESS_TOKEN_SECRET"],
)

anchor_tweet = client.create_tweet(text=tweet_text)

client.create_tweet(text=tweet_text, 
                    in_reply_to_tweet_id=anchor_tweet.data['id'])
