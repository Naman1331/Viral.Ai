import pyyoutube
import strict_rfc3339
import datetime

"""INSTALLATION INSTRUCTIONS
pip install --upgrade python-youtube
pip install strict_rfc3339

Refer to this for assistance:
https://github.com/sns-sdks/python-youtube/blob/master/pyyoutube/api.py
https://developers.google.com/youtube/v3/docs/search/list#type
"""


def __convert_timestamp_to_rfc3339(timestamp: datetime) -> str:
    """
    The Youtube API requires users to specify all times in RFC3339 format.
    """
    ts = datetime.datetime.timestamp(timestamp)
    return strict_rfc3339.timestamp_to_rfc3339_utcoffset(ts)


def search(API_KEY: str, QUERIES: list, VIDEO_DURATION="short", DAYS=30) -> list:
    """
    Searches the Youtube API for the most relevant shorts

    API_KEY: use your API key. Or use this example: AIzaSyAkXaZeu-eAQriePDY3A5PcqVY6f3_Qukw
    VIDEO_DURATION: options are any, long, medium, short
    DAYS: only videos are shown that have been created in the last x days
    QUERIES: ex: ["fortnite", "skibidi"]
    """
    videos = {}
    api = pyyoutube.Api(api_key=API_KEY)
    published_after = __convert_timestamp_to_rfc3339(
        datetime.datetime.now() - datetime.timedelta(days=DAYS)
    )
    queries = "|".join(QUERIES)
    res = api.search(
        q=queries,
        limit=50,
        count=50,
        order="viewCount",
        published_after=published_after,
        video_duration=VIDEO_DURATION,
        search_type="video",
    )
    for item in res.items:
        if item.id.videoId:
            videos[item.id.videoId] = {
                "title": item.snippet.title,
                "channelId": item.snippet.channelId,
                "description": item.snippet.description,
                "thumbnails": item.snippet.thumbnails,
            }

    return videos