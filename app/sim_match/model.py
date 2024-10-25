from sentence_transformers import SentenceTransformer

from config import EmbeddingConfig


class SimMatchModel(object):
    def __init__(self):
        self.embedding_model = SentenceTransformer(EmbeddingConfig.bge_zh_large)
