import asyncio
from twikit import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Login credentials
USERNAME = os.environ['X_USERNAME']
EMAIL  = os.environ['X_EMAIL']
PASSWORD = os.environ['X_PASSWORD']

# Initialize client
client = Client('en-US')

async def login(client, cookie_path: str = 'data/cookies.json'):
    if os.path.exists(cookie_path):
        client.load_cookies(cookie_path)
    else:
        await client.login(
            auth_info_1=USERNAME ,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
        client.save_cookies('data/cookies.json')

asyncio.run(login(client))