from pytube import YouTube
from pytube.innertube import _default_clients
import os
from pathlib import Path
import config
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
"""INSTALLATION
pip install pytube"""

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]




def delete_files(path: str):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        os.remove(file_path)


def download(id, save_path):
    youtubeObject = YouTube("https://www.youtube.com/shorts/" + id)
    if config.VIDEO_QUALITY == "LOW":
        youtubeObject = youtubeObject.streams.get_lowest_resolution()
    else:
        youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        # Download the video
        youtubeObject.download(output_path = save_path, filename = id + ".mp4")
        print('Video downloaded successfully!')
    except:
        print("Some Error!")    
    

