import config
import generate_keywords
import video_details
import download_links
import video_links
import compare, numpy as np
import threading
import os
import similarity_search
from pathlib import Path
import reflex as rx



def main():
    config.PERCENT_COMPLETED = 0
    config.CURRENT_STATUS = "None"
    download_links.delete_files(config.FULL_PATH)
    
    response = generate_keywords.generate_keywords(config.FULL_USER_VIDEO) #list of key words
    config.PERCENT_COMPLETED = 10
    config.CURRENT_STATUS = "Generated Key Words: " + str(response)
    rx.console_log(str(config.PERCENT_COMPLETED) + "%: " + config.CURRENT_STATUS)

    print(response)

    
    videoDatabase = video_links.search(config.API_KEY, response) #50 top videos
    print(videoDatabase)


    config.PERCENT_COMPLETED = 40
    config.CURRENT_STATUS = "Downloading Videos"
    rx.console_log(str(config.PERCENT_COMPLETED) + "%: " + config.CURRENT_STATUS)
    for key, value in videoDatabase.items():
        try:
            print("Downloading Video: " + key)
            print("Video Image: " + value["thumbnails"].default.url)
            print("Video Information: " + str(value))
            download_links.download(key, config.FULL_PATH) #downloading all the 50 videos

        except Exception as e:
            print("Video " + key + " couldnt be downloaded: " + str(e))
    

    
    config.PERCENT_COMPLETED = 75
    config.CURRENT_STATUS = "Performing Similarity Search"
    rx.console_log(str(config.PERCENT_COMPLETED) + "%: " + config.CURRENT_STATUS)
    closest_videos = similarity_search.similarity_search()
    print(closest_videos)
    # extract video details
    vid_dict = {}
    for x in closest_videos:
        id = Path(x).stem
        vid_dict[id] = video_details.video(id, config.API_KEY)
    config.PERCENT_COMPLETED = 94
    config.CURRENT_STATUS = "Results coming soon!"
    rx.console_log(str(config.PERCENT_COMPLETED) + "%: " + config.CURRENT_STATUS)

    result = compare.compare(vid_dict, "la-hacks-420908", "us-central1", response)
    
    config.PERCENT_COMPLETED = 100
    config.CURRENT_STATUS = ""
    rx.console_log(str(config.PERCENT_COMPLETED) + "%: " + config.CURRENT_STATUS)
    print(result)
    return result, vid_dict

