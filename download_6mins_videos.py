import subprocess
import pandas as pd
from datetime import datetime, timedelta
import os
import tqdm
from time import sleep
import random
import glob

def extract_video_id(video_url):
    if "v=" in video_url:
        return video_url.split("v=")[1]
    elif "shorts" in video_url:
        return video_url.split("/")[-1]
    else:
        return None

def download(video_id, video_url, duration_in_sec):
    
    command = [
        'yt-dlp',
        video_url,
        '-o', f'iraqi_videos_6mins/{video_id}.%(ext)s'
    ]

    if duration_in_sec:
        if duration_in_sec > 360:
            command.extend(['--download-sections', f'*0-360'])
    
    try:
        subprocess.run(command, check=True)
        print(f"Successfully downloaded {video_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
    except FileNotFoundError:
        print("Error: yt-dlp is not installed or not in PATH")

# Example usage
# video_url = "https://www.youtube.com/watch?v=example"
# download(video_url)

def get_processed_video_ids():
    videos = list(glob.glob("iraqi_videos_6mins/*.*"))
    return set([video.split("/")[-1].split(".")[0] for video in videos])

if __name__ == "__main__":
    df = pd.read_csv("iraqi_channels_videos_presampled.csv")
    processed_video_ids = get_processed_video_ids()
    for index, row in tqdm.tqdm(df.iterrows()):
        video_id = extract_video_id(row["video_url"])
        if video_id is None:
            print(f"Skipping {row['video_url']} because it doesn't contain video id")
            continue
        if video_id in processed_video_ids:
            print(f"Skipping {row['video_url']} because it has already been processed")
            continue
        download(video_id, row["video_url"], row["duration_in_sec"])
        sleep(random.randint(5, 10))