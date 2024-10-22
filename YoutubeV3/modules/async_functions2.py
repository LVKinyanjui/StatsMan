import aiohttp
import asyncio
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
CONCURRENCY_LIMIT = 5

# Asynchronous function to fetch video IDs from a playlist
async def afetch_video_ids(session, playlist_id, page_token=None):
    url = (
        f"{BASE_URL}?part=contentDetails"
        f"&playlistId={playlist_id}"
        f"&key={API_KEY}"
        f"&maxResults=50"
    )
    
    # Add page token if pagination is required
    if page_token:
        url += f"&pageToken={page_token}"
    
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error: {response.status}, {await response.text()}")
            return None

# Main function to get video IDs from the uploads playlist
async def aget_video_ids_from_playlist(playlist_id):
    video_ids = []
    next_page_token = None

    async with aiohttp.ClientSession() as session:
        while True:
            data = await afetch_video_ids(session, playlist_id, next_page_token)
            
            if data:
                # Collect video IDs from the current page
                video_ids += [item['contentDetails']['videoId'] for item in data['items']]
                
                # Check if there's another page of results
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break
            else:
                break

    return video_ids

# Entry point to run the asynchronous function
if __name__ == "__main__":
    uploads_playlist_id = 'UUwA8PYIymQEXh7jwcrIUDHg'  # Replace with your playlist ID

    # Run the asynchronous event loop to get video IDs
    video_ids = asyncio.run(aget_video_ids_from_playlist(uploads_playlist_id))

    print(f"Retrieved {len(video_ids)} video IDs.")
    for video_id in video_ids:
        print(video_id)
