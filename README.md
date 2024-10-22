
# RAG 项目

本项目是一个基于 Retrieval-Augmented Generation (RAG) 模型的文本处理工具，包含重排序（Rerank）、相似度匹配（Similarity Matching）、文本分割（Text Splitting）等功能。

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
│   │   └── 四种通知的层级体系.docx # 示例文档
│   ├── index                 # 索引数据目录
│   │   └── data.index        # 索引文件
│   └── pdf                   # PDF 文档存储
│       ├── AF01.pdf          # 示例 PDF 文件
│       └── ...               # 其他 PDF 文件
├── demo.py                   # 项目演示脚本
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

## 安装

1. 克隆本项目代码：
   ```bash
   git clone https://github.com/yourusername/rag_project.git
   cd rag_project
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

1. 运行项目的主脚本 `main.py` 来进行全文检索和生成任务：
   ```bash
   python main.py
   ```


## 贡献指南

如果你想为本项目贡献代码，请先 Fork 本仓库并提交 Pull Request。确保代码格式符合项目的要求，并通过所有测试。

## 许可证

本项目遵循 MIT 许可证。
