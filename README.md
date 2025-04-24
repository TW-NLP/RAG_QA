
# RAG 项目

本项目是一个基于 Retrieval-Augmented Generation (RAG) 模型的文本处理工具，主要用于文本检索与生成，包含以下功能模块：
- **重排序（Rerank）**：对检索结果进行重新排序，以提高结果的相关性。
- **相似度匹配（Similarity Matching）**：基于嵌入模型计算文本的相似度。
- **文本分割（Text Splitting）**：将长文本分割为适合处理的较小段落。

本项目可以处理多种数据源，比如非结构化的PDF、Docx等，通过切片和排序等策略，获取与问题最相关的答案，并集成VLLM来对开源的大模型进行推理。

## 目录结构

项目的主要代码和文件组织如下：

```
├── app
│   ├── rerank                # 重排序模块
│   │   └── model.py          # 重排序模型代码
│   ├── sim_match             # 相似度匹配模块
│   │   └── model.py          # 相似度匹配模型代码
│   └── text_split            # 文本分割模块
│       ├── __pycache__       # Python 缓存文件
│       └── split.py          # 文本分割实现
├── config.py                 # 项目配置文件
├── data
│   ├── doc                   # 文档存储目录
│   │   └── pycharm.docx # 示例文档
│   ├── index                 # 索引数据目录
│   │   └── data.index        # 索引文件
│   └── pdf                   # PDF 文档存储
│       ├── AF01.pdf          # 示例 PDF 文件
│       └── ...               # 其他 PDF 文件
├── main.py                   # 主运行脚本
├── pre_model                 # 预训练模型
│   ├── embedding_model       # 嵌入模型目录
│   │   └── bge-large-zh      # 中文大规模嵌入模型
│   │       └── ...           # 嵌入模型相关文件
│   └── rerank_model          # 重排序模型目录
│       └── rerank_large      # 大规模重排序模型
│           └── ...           # 重排序模型相关文件
└── requirements.txt          # 项目依赖文件
```
项目线路如下：
<p align="center">
  <img src="images/传统RAG.drawio.png" alt="传统RAG" width="800"/>
</p>
## 安装

1. 克隆本项目代码：
   ```bash
   git clone https://github.com/TW-NLP/RAG_QA
   cd RAG_QA
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 模型权重下载：
   - 需要从 [huggingface.co](https://huggingface.co/BAAI/bge-large-zh-v1.5) 下载 `pytorch_model.bin` 文件，并放入 `pre_model/embedding_model/bge-large-zh` 目录下。
   - 需要从 [huggingface.co](https://huggingface.co/BAAI/bge-reranker-large) 下载 `pytorch_model.bin` 文件，并放入 `pre_model/rerank_model/rerank_large` 目录下。

## 使用说明

1. 运行项目的主脚本 `main.py` 来进行全文检索和生成任务：
   ```bash
   python main.py
   ```
## 路线图

- [X] 支持bge embedding
- [X] 支持 rerank
- [X] 支持 Docx、PDF的处理
- [ ] 支持 大模型的切片
- [ ] 添加大模型的推理

## 贡献指南

如果你想为本项目贡献代码，请先 Fork 本仓库并提交 Pull Request。确保代码格式符合项目的要求，并通过所有测试。

## 许可证

本项目遵循 MIT 许可证。
