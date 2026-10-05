"""inverted_index: 倒排索引构建/查询 CLI。"""
from .index import InvertedIndex, Posting
from .query import boolean_query, phrase_query

__all__ = ["InvertedIndex", "Posting", "boolean_query", "phrase_query"]
__version__ = "0.1.0"
