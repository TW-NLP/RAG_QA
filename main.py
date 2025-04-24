import os
from sentence_transformers import SentenceTransformer

from app.rerank.model import ReRankModel
from app.sim_match.model import SimMatchModel
from app.text_split.split import TextSplit
from config import PDF_DATA_DIR, DOC_DATA_DIR, EmbeddingConfig, ReRankConfig, FAISS_SAVE_DIR, SEARCH_TOPK, RESULT_TOPK
from tqdm import tqdm
from FlagEmbedding import FlagReranker
import numpy as np
import faiss
import jieba
from rank_bm25 import BM25Okapi


class RAGDocQA(object):
    def __init__(self, data_path_list):
        """RAG document QA

        Args:
            data_path_list (list): [PDF_PATH,DOC_PATH]
            embedding_path (str): sentence embedding model path
            rerank_path (_str): rerank model path
        """

        self.data_path_list = data_path_list
        self.text_split = TextSplit()
        self.sim_model = SimMatchModel()
        self.rank_model = ReRankModel()

    def vector_search(self, query, data_list):
        """use vector search

        Args:
            query (str): 
            data_list (list): data sum list

        Returns:
            list: vector search list
        """
        # 从文件中加载 FAISS 索引
        index = faiss.read_index(FAISS_SAVE_DIR)

        # 将查询文本编码为嵌入向量
        query_embedding = self.sim_model.embedding_model.encode([query], normalize_embeddings=True)

        # 进行最近邻搜索，返回前 3 个相似的文本
        D, I = index.search(np.array(query_embedding), SEARCH_TOPK)

        return [data_list[i] for i in I[0]]

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

    def rerank(self, query, passages):

        """rerank vector、bm25 results

        Args:
            query (str): question
            passages (list): search list

        Returns:
            list: rerank scores list
        """
        # 将 query 与 passages 进行 rerank
        inputs = [[query, passage] for passage in passages]
        scores = self.rank_model.rerank_model.compute_score(inputs)
        return scores

    def search(self, query, bm25, data_list):

        """ sum vector、bm25 、rerank search

        Args:
            query (str): question
            bm25 (object): bm25
            data_list (list): data list
        """
        search_sum = []
        vector_search_result = self.vector_search(query, data_list)
        keyword_search_result = self.keyword_search(query, bm25, data_list)
        search_sum.extend(vector_search_result)
        search_sum.extend(keyword_search_result)

        rerank_score = self.rerank(query, search_sum)

        sorted_results = sorted(zip(search_sum, rerank_score), key=lambda x: x[1], reverse=True)[:RESULT_TOPK]

        return sorted_results

    def vector_write(self, data_list):

        embeddings = []
        for data_i in tqdm(data_list):
            embedding_i = self.sim_model.embedding_model.encode(data_i, normalize_embeddings=True)
            embeddings.append(embedding_i)

        embeddings = np.array(embeddings)

        # 创建 FAISS 索引 (L2 距离)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)

        # 将向量添加到索引中
        index.add(embeddings)

        # 检查是否已经存在索引文件，存在则删除
        if os.path.exists(FAISS_SAVE_DIR):
            print(f"索引文件已存在，删除旧的索引文件：{FAISS_SAVE_DIR}")
            os.remove(FAISS_SAVE_DIR)

        # 持久化索引
        faiss.write_index(index, FAISS_SAVE_DIR)

        # bm25
        # 定义 BM25 搜索的分词器和索引器
        tokenized_corpus = [list(jieba.cut(text)) for text in data_list]  # 对所有文本进行分词
        bm25 = BM25Okapi(tokenized_corpus)  # 创建 BM25 索引
        return bm25

    def data_convert(self):
        data_sum = []
        pdf_path = self.data_path_list[0]
        doc_path = self.data_path_list[1]

        # 文档的处理方式，可以进行如下的选择
        for path_i in os.listdir(pdf_path):
            pdf_result = self.text_split.pdf_split(os.path.join(pdf_path, path_i))
            data_sum.extend(pdf_result)

        for path_i in os.listdir(doc_path):
            doc_result = self.text_split.doc_split(os.path.join(doc_path, path_i))
            data_sum.extend(doc_result)

        bm25 = self.vector_write(data_sum)
        return bm25, data_sum


if __name__ == '__main__':
    data_path = [PDF_DATA_DIR, DOC_DATA_DIR]

    query = "网络安全是什么？"

    qa_model = RAGDocQA(data_path)
    # 文件向量化
    print("***文本持久化中*****")
    bm25, data_sum = qa_model.data_convert()
    # bge search
    print("***问题搜索中***")
    search_list = qa_model.search(query, bm25, data_sum)
    print(f"搜索的结果集合为：{search_list}")
