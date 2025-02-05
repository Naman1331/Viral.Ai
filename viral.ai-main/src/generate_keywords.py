from google.cloud import aiplatform
import vertexai.preview
from vertexai.generative_models import GenerativeModel, Part
from pathlib import Path
import json
import config


SERVER_NAME = "la-hacks-420908"
SERVER_LOCATION = "us-central1"

"""INSTALLATION
pip install --upgrade google-cloud-aiplatform"""
def mp4_to_bytes(file_path):
    with open(file_path, "rb") as file:
        mp4_bytes = file.read()
    return mp4_bytes

def generate_keywords(file_path: str,project_id=SERVER_NAME, location= SERVER_LOCATION):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Load the model
    model = GenerativeModel(model_name="gemini-1.5-pro-preview-0409")

    prompt = """
      Generate keywords for the video in the form of a JSON array. Return nothing except the array."
      
    """

    video_file_path = file_path

    video_file = Part.from_data(mp4_to_bytes(video_file_path), mime_type = "video/mp4")

    contents = [video_file, prompt]

    response = model.generate_content(contents)
    try:
        return json.loads(response.text)
    except:
        print("ERROR LOADING RESPONSE INTO JSON")


