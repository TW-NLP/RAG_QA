from FlagEmbedding import FlagReranker

from config import ReRankConfig


class ReRankModel(object):
    def __init__(self):
        self.rerank_model = FlagReranker(ReRankConfig.rerank_large, use_fp16=True)
