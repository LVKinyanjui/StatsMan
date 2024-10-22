import asyncio
import aiohttp
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3/videos"

# Asynchronous function to fetch video stats for a batch of 50 video IDs
async def afetch_batch(session, video_ids):
    url = (
        f"{BASE_URL}?part=statistics,contentDetails,snippet"
        f"&id={','.join(video_ids)}"
        f"&key={API_KEY}"
    )

    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data['items']
        else:
            print(f"Error: {response.status}, {await response.text()}")
            return []

# Function to get video stats asynchronously
async def aget_video_stats(video_ids, concurrency_limit=10):
    video_stats = []
    
    # Break the list of video IDs into chunks of 50
    video_id_batches = [video_ids[i:i + 50] for i in range(0, len(video_ids), 50)]
    
    # Create a semaphore to limit the number of concurrent requests
    semaphore = asyncio.Semaphore(concurrency_limit)

    async with aiohttp.ClientSession() as session:
        # Create tasks for each batch of video IDs
        tasks = [
            afetch_with_limit(semaphore, afetch_batch, session, batch)
            for batch in video_id_batches
        ]
        
        # Gather all results asynchronously
        results = await asyncio.gather(*tasks)

    # Collect stats from all batches
    for batch_result in results:
        for item in batch_result:
            stats = {
                'videoId': item['id'],
                'viewCount': item['statistics'].get('viewCount', 0),
                'likeCount': item['statistics'].get('likeCount', 0),
                'commentCount': item['statistics'].get('commentCount', 0),
                'duration': item['contentDetails']['duration'],
                'videoTitle': item['snippet']['title'],
                'publishedAt': item['snippet']['publishedAt'],
            }
            video_stats.append(stats)
    
    return video_stats

# Helper function to limit concurrent requests
async def afetch_with_limit(semaphore, fetch_fn, *args):
    async with semaphore:
        return await fetch_fn(*args)

# Entry point to run the asynchronous function
if __name__ == "__main__":
    video_ids = ['dQw4w9WgXcQ', '_YLy_Q5FhAg', "dKCa85zxFQo",]  # Replace with your video IDs

    # Run the asynchronous event loop
    stats = asyncio.run(aget_video_stats(video_ids))

    for video in stats:
        print(video)
        print("-" * 40)
