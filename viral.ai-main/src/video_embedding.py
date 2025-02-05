from typing import Optional
import config

import vertexai
from vertexai.vision_models import (
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
    Video,
    VideoSegmentConfig,
)

class VideoSegmentConfig:
    def __init__(self, start_offset_sec: int, end_offset_sec: int, interval_sec: int):
        self.start_offset_sec = start_offset_sec
        self.end_offset_sec = end_offset_sec
        self.interval_sec = interval_sec
def get_video_embeddings(
    video_path: str,
    project_id: Optional[str] = "la-hacks-420908",
    location: Optional[str] = "us-central1",
    contextual_text: Optional[str] = None,
    dimension: Optional[int] = 1408,
    video_segment_config: Optional[VideoSegmentConfig] = VideoSegmentConfig(0, 60, 60),
) -> MultiModalEmbeddingResponse:
    """Example of how to generate multimodal embeddings from video and text.

    Args:
        project_id: Google Cloud Project ID, used to initialize vertexai
        location: Google Cloud Region, used to initialize vertexai
        video_path: Path to video (local or Google Cloud Storage) to generate embeddings for.
        contextual_text: Text to generate embeddings for.
        dimension: Dimension for the returned embeddings.
            https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-multimodal-embeddings#low-dimension
        video_segment_config: Define specific segments to generate embeddings for.
            https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-multimodal-embeddings#video-best-practices
    """
    vertexai.init(project=project_id, location=location)

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    video = Video.load_from_file(video_path)

    embeddings = model.get_embeddings(
        video=video,
        video_segment_config=video_segment_config,
        contextual_text=contextual_text,
        dimension=dimension,
    )

    # Video Embeddings are segmented based on the video_segment_config.
    print("Video Embeddings:")
    for video_embedding in embeddings.video_embeddings:
        print(
            f"Video Segment: {video_embedding.start_offset_sec} - {video_embedding.end_offset_sec}"
        )
        print(f"Embedding: {video_embedding.embedding}")

    print(f"Text Embedding: {embeddings.text_embedding}")
    return embeddings.video_embeddings[0].embedding, video_path


if __name__ == "__main__":
    embedding, path = get_video_embeddings(str(config.FULL_PATH))

