from app.rag.keyword_search import KeyWordSearch
from app.rag.vector_search import VectorSearch
from config import RESULT_TOPK


class RagSearch(object):

    def __init__(self, faiss_path, embedding_model, rank_model):
        """

        :param faiss_path: faiss 路径
        :param embedding_model: embedding 模型
        :param rank_model: rerank 模型
        """
        self.key_search = KeyWordSearch()
        self.vector_search = VectorSearch(faiss_path, embedding_model)
        self.rerank_model = rank_model

    def search(self, query, bm25, data_list):
        """ sum vector、bm25 、rerank search

        Args:
            query (str): question
            bm25 (object): bm25
            data_list (list): data list
        """
        search_sum = []
        vector_search_result = self.vector_search.simple_vector_search(query, data_list)
        keyword_search_result = self.key_search.keyword_search(query, bm25, data_list)
        search_sum.extend(vector_search_result)
        search_sum.extend(keyword_search_result)

        search_res = self.rerank(query, search_sum)

        return search_res

    def rerank(self, query, search_sum):
        """rerank vector、bm25 results

        Args:
            query (str): question
            search_sum (list): search list

        Returns:
            list: rerank scores list
        """
        # 将 query 与 passages 进行 rerank
        inputs = [[query, passage] for passage in search_sum]
        scores = self.rerank_model.compute_score(inputs)

        sorted_results = sorted(zip(search_sum, scores), key=lambda x: x[1], reverse=True)[:RESULT_TOPK]
        return sorted_results
