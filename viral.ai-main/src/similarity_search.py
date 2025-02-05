import towhee
from towhee import pipe, ops, DataCollection
import numpy  as np
from sklearn import preprocessing
import random
import faiss
from math import sqrt
from video_embedding import get_video_embeddings
import config
import concurrent.futures
import config
import generate_keywords
import video_details
import download_links
import video_links
import compare, numpy as np
import os

def similarity_search():
    video_path = []
    video_embeddings = []
    k = config.CONSTANT_X
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
        video_files = os.listdir(config.FULL_PATH)
        future_to_file = {executor.submit(get_video_embeddings, os.path.join(config.FULL_PATH, filename)): filename for filename in video_files}
        for future in concurrent.futures.as_completed(future_to_file):
            try:
                embedding, path = future.result()
                video_path.append(path)
                video_embeddings.append(embedding)
            except Exception as e:
                print(str(e))

    clip_embeds= np.array(video_embeddings)
    clip_paths = np.array(video_path)
    print(clip_embeds)
    #print(clip_paths)
    #print(dict_video_embeddings)
    print(clip_embeds.shape)

    #FAISS
    num_vectors,  feat_dim = clip_embeds.shape
    quantize = faiss.IndexFlatIP(feat_dim)
    #ivf_index.train(clip_embeds)
    #ivf_index.add(clip_embeds)

    #target video embedding
    query_embed, query_path = get_video_embeddings(str(config.USER_VIDEO))
    query_embed = np.array(query_embed).reshape(1, -1)
    topk_videos = []
    if k > 10000:
        ###FAISS IVF
        ivf_index = faiss.IndexIVFFlat(quantize, feat_dim, int(sqrt(num_vectors)), faiss.METRIC_L2)
        ivf_index.train(clip_embeds)
        ivf_index.add(clip_embeds)
        FAISS_index = {
            "video_ids": clip_paths,
            "clip_embeds": ivf_index,
        }
        test, topk_indices = FAISS_index["clip_embeds"].search(query_embed, k)
        topk_videos = [FAISS_index["video_ids"][i] for i in topk_indices[0]]
    else:
        #FAISS FLATL2
        ivf_index = faiss.IndexFlatL2(feat_dim)
        ivf_index.add(clip_embeds)
        FAISS_index = {
            "video_ids": clip_paths,
            "clip_embeds": ivf_index,
        }
        test, topk_indices = FAISS_index["clip_embeds"].search(query_embed, k)
        topk_videos = [FAISS_index["video_ids"][i] for i in topk_indices[0]]

    #Closest 30 videos is hardcoded for now
    return topk_videos



