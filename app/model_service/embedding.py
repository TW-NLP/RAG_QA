from FlagEmbedding import FlagReranker
from sentence_transformers import SentenceTransformer

from config import ReRankConfig, EmbeddingConfig


class EmbeddingModel(object):
    def __init__(self):
        self.embedding_model = SentenceTransformer(EmbeddingConfig.bge_zh_large)
        self.rank_model = FlagReranker(ReRankConfig.rerank_large, use_fp16=True)
