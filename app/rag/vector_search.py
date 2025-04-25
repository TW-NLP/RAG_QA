import faiss
import numpy as np

from config import SEARCH_TOPK


class VectorSearch(object):
    """
    向量搜索
    """

    def __init__(self, faiss_path, embedding_model):
        """

        :param faiss_path: faiss 数据持久化路径
        :param embedding_model: embedding 模型
        """

        self.faiss_path = faiss_path
        self.embedding_model = embedding_model

    def simple_vector_search(self, query, data_list):
        """use vector search

        Args:
            query (str):
            data_list (list): data sum list

        Returns:
            list: vector search list
        """
        # 从文件中加载 FAISS 索引
        index = faiss.read_index(self.faiss_path)

        # 将查询文本编码为嵌入向量
        query_embedding = self.embedding_model.encode([query], normalize_embeddings=True)

        # 进行最近邻搜索，返回前 SEARCH_TOPK 个相似的文本
        D, I = index.search(np.array(query_embedding), SEARCH_TOPK)

        return [data_list[i] for i in I[0]]
