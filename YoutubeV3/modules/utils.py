import re

def extract_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube URL. This function supports the following patterns:
    - https://youtube.com/watch?v={video_id}
    - https://youtube.com/embed/{video_id}
    - https://youtu.be/{video_id}
    - https://youtube.com/shorts/{video_id}
    :param str url: A YouTube URL containing a video id.
    :return: The video id as a string.
    """
    # Regular expression pattern to match YouTube video IDs (regular videos and Shorts)
    pattern = re.compile(r"(?:(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/))|(?:youtu\.be\/))([\w\-]+)")
    
    match = pattern.search(url)
    if match:
        return match.group(1)
    else:
        print("Error: Invalid YouTube video link.")
        return ""

if __name__ == "__main__":
    print(extract_video_id("https://www.youtube.com/watch?v=M4HGJehH4r0"))
    print(extract_video_id("https://www.youtube.com/shorts/NkIM3-tp-WQ"))
    print(extract_video_id("https://youtube.com/shorts/NkIM3-tp-WQ?si=YrQvXNJ0QqUnjAE9"))