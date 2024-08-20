from twikit import Client, TooManyRequests
from twikit_login import login
import time
from datetime import datetime
import json
import asyncio
from random import randint

from dotenv import load_dotenv
import os

load_dotenv()

# Login credentials
username = os.environ['X_USERNAME']
email = os.environ['X_EMAIL']
password = os.environ['X_PASSWORD']

MINIMUM_TWEETS = 5
QUERY = '(from:elonmusk) lang:en until:2024-07-19 since:2018-01-01'


async def get_tweets(tweets, client):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets


async def main():
    #* authenticate to X.com
    #! 1) use the login credentials. 2) use cookies.
    client = Client(language='en-US')
    
    login(client)

    tweet_count = 0
    tweets = None
    tweet_data = []

    while tweet_count < MINIMUM_TWEETS:

        try:
            tweets = await get_tweets(tweets, client)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data.append(
                {
                    "tweet_count": tweet_count, 
                    "user_name": tweet.user.name, 
                    "tweet_text": tweet.text, 
                    "created_at": tweet.created_at, 
                    "retweet_count": tweet.retweet_count, 
                    "favourite_count": tweet.favorite_count
                }
            )
            

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')

    # SAVE DATA
    with open("data/tweets.jsonl", "w", encoding="utf-8") as fp:
        for tweet in tweet_data:
            json.dump(tweet, fp)

if __name__ == '__main__':
    asyncio.run(main())