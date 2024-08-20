from twikit import Client
from twikit_login import login
import asyncio

async def asearch_tweets(client):
    tweets = await client.search_tweet('python', 'Latest')

    for tweet in tweets:
        print(
            tweet.user.name,
            tweet.text,
            tweet.created_at
        )

if __name__ == '__main__':
    client = Client('en-US')
    login(client)
    asyncio.run(asearch_tweets(client))