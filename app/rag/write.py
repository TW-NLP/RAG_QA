import os
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from tqdm import tqdm
import jieba

from app.utils.file_split import TextSplit
from config import FAISS_SAVE_DIR


class DataWrite(object):
    """
    数据持久化
    """

    def __init__(self, embedding_model):
        """

        :param embedding_model: embedding 模型
        """
        self.embedding_model = embedding_model
        self.text_split = TextSplit()

    def vector_write(self, data_list):

        embeddings = []
        for data_i in tqdm(data_list):
            embedding_i = self.embedding_model.encode(data_i, normalize_embeddings=True)
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

    def data_convert(self, data_path_list):
        """

        :param data_path_list: 数据路径
        :return:
        """
        data_sum = []
        pdf_path = data_path_list[0]
        doc_path = data_path_list[1]

        # 文档的处理方式，可以进行如下的选择
        for path_i in os.listdir(pdf_path):
            pdf_result = self.text_split.pdf_split(os.path.join(pdf_path, path_i))
            data_sum.extend(pdf_result)

        for path_i in os.listdir(doc_path):
            doc_result = self.text_split.doc_split(os.path.join(doc_path, path_i))
            data_sum.extend(doc_result)

        bm25 = self.vector_write(data_sum)
        return bm25, data_sum
