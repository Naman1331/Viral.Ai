from google.cloud import aiplatform
import vertexai.preview
from vertexai.generative_models import GenerativeModel, Part
from pathlib import Path
import config



"""INSTALLATION
pip install --upgrade google-cloud-aiplatform"""
safety_config = {

    vertexai.generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: vertexai.generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    vertexai.generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: vertexai.generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    vertexai.generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: vertexai.generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    vertexai.generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: vertexai.generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}

def mp4_to_bytes(file_path):
    with open(file_path, "rb") as file:
        mp4_bytes = file.read()
    return mp4_bytes


def compare(d: dict ,project_id: str, location: str, keywords:list):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name="gemini-1.5-pro-preview-0409")
    prompt = f"""
      {str(config.CONSTANT_X + 1)} videos have been uploaded. The first {str(config.CONSTANT_X)} videos have been widely successful and have gone viral on youtube. All the videos have common themes of {str(keywords)}.
      Each of the successful videos is uploaded according to it's unique ID, in the form [id].mp4, while the new video is called new_video.mp4, and it hasn't been uploaded to youtube yet.
      Here are details on the characteristics of each video, which have contributed to their popularity. 
      {str(d)}.

      new_video.mp4 is one that has been recently created with the intent of going viral, and it is similar to the first {str(config.CONSTANT_X)} videos.
      Follow these steps:
      1. Analyze all the videos and determine how the last video (the newly created one) can be modified to go viral. Be sure to reference the other videos in the response, using specific examples and citing video IDs in the form https://www.youtube.com/shorts/[id]
      2. Given the characteristics of the first {str(config.CONSTANT_X)} videos, generate an ideal title and an ideal description for the video, which will help it achieve success when it is uploaded to youtube.


      All in all, make sure to not provide general feedback, but be as specific as possible relating to the videos.
    """

    contents = []
    for key, value in d.items():
        contents.append(Part.from_data(mp4_to_bytes(config.FULL_PATH + "/" + key + ".mp4"), mime_type = "video/mp4"))

    contents.append(Part.from_data(mp4_to_bytes(config.FULL_USER_VIDEO), mime_type = "video/mp4"))

    contents.append(prompt)
    response = model.generate_content(contents, safety_settings=safety_config)
    return response.text.replace("new_video.mp4", "your video")

