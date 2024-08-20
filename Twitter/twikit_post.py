from twikit import Client
from twikit_login import login
from uuid import uuid4
import asyncio

async def apost(client):
    # Create a tweet with the provided text and attached media
    await client.create_tweet(
        text='Its super cold today, is Poseidon doing his thing?',
        media_ids=str(uuid4())
    )

if __name__ == '__main__':
    client = Client('en-US')
    login(client)
    asyncio.run(apost(client))