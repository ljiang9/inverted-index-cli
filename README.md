# inverted-index-cli

零依赖的倒排索引构建与查询 CLI。对目录下 `.txt`/`.md` 文档分词，构建 `term → {doc_id: [positions]}` 倒排表并持久化；支持布尔查询（AND/OR/NOT）与短语查询。

## 快速开始

```bash
python -m inverted_index build ./docs --out idx.json
python -m inverted_index query "python -java" --index idx.json
python -m inverted_index phrase "python 与 java" --index idx.json
```

## 无 API Key 如何运行

本工具完全离线，所有索引构建与查询都在本地完成，不需要任何 API Key。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © ljiang9
