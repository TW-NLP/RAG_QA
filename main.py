import os

from app.model_service.embedding import EmbeddingModel
from app.rag.search import RagSearch
from app.rag.write import DataWrite
from config import PDF_DATA_DIR, DOC_DATA_DIR, FAISS_SAVE_DIR, SEARCH_TOPK, RESULT_TOPK, EmbeddingConfig, logger


class RagQA(object):
    def __init__(self, data_path, faiss_path):
        """
        :param data_path:
        :param faiss_path:
        """
        self.data_path = data_path

        self.model = EmbeddingModel()

        self.write_engine = DataWrite(self.model.embedding_model)

        self.search_engine = RagSearch(faiss_path, self.model.embedding_model, self.model.rank_model)

    def data_save(self):
        bm25, data_summary = self.write_engine.data_convert(self.data_path)
        return bm25, data_summary


if __name__ == '__main__':
    data_path = [PDF_DATA_DIR, DOC_DATA_DIR]

    query = "网络安全是什么？"

    qa_engine = RagQA(data_path, FAISS_SAVE_DIR)
    logger.info('文本向量化中！！！')
    bm25_engine, data_sum = qa_engine.data_save()
    logger.info('文本向量化完成！！！')
    # bge search
    print("***问题搜索中***")
    search_list = qa_engine.search_engine.search(query, bm25_engine, data_sum)
    print(f"搜索的结果集合为：{search_list}")
