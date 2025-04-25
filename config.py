import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAG_QA")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

PDF_DATA_DIR = os.path.join(PROJECT_DIR, "data", "pdf")

DOC_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'doc')

FAISS_SAVE_DIR = os.path.join(PROJECT_DIR, 'data', 'index', 'data.index')

SEARCH_TOPK = 20
RESULT_TOPK = 10


class EmbeddingConfig(object):
    embedding_path = os.path.join(PROJECT_DIR, 'pre_model', 'embedding_model')
    bge_zh_large = os.path.join(embedding_path, 'bge-large-zh')


class ReRankConfig(object):
    rerank_path = os.path.join(PROJECT_DIR, 'pre_model', 'rerank_model')
    rerank_large = os.path.join(rerank_path, 'bge_rerank')


