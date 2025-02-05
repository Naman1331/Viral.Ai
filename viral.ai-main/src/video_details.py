import pyyoutube

def video(id:str, api_key: str) -> dict:

    '''example response
{'likeCount': 2934, 'viewCount': 60893, 'dislikeCount': None, 'commentCount': 37}


    '''
    api = pyyoutube.Api(api_key=api_key)
    videoListResponse = api.get_video_by_id(video_id=id)

    print(videoListResponse.items[0].statistics.likeCount)
    statistics = {"likeCount":videoListResponse.items[0].statistics.likeCount, "viewCount":videoListResponse.items[0].statistics.viewCount,"commentCount":videoListResponse.items[0].statistics.commentCount}
    return statistics


