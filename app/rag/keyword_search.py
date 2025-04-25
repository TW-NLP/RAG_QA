import jieba
import numpy as np

from config import SEARCH_TOPK


class KeyWordSearch(object):
    """
    关键词搜索
    """

    def __init__(self):
        pass

    def keyword_search(self, query, bm25, data_list):
        """use bm25 search

        Args:
            query (str): question
            bm25 (object): bm25
            data_list (list): data list

        Returns:
            list: bm25 search list
        """
        tokenized_query = list(jieba.cut(query))  # 对查询文本进行分词
        bm25_scores = bm25.get_scores(tokenized_query)  # 获取 BM25 分数
        top_n = np.argsort(bm25_scores)[::-1][:SEARCH_TOPK]  # 获取前 3 个分数最高的索引

        return [data_list[i] for i in top_n]
