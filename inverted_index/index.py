"""倒排索引：term -> {doc_id: [positions]}，持久化为 JSON。"""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field, asdict
from pathlib import Path

_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]")

def tokenize(text): return _TOKEN_RE.findall(text.lower())

@dataclass
class Posting:
    doc_id: str
    positions: list[int] = field(default_factory=list)

class InvertedIndex:
    def __init__(self):
        self.postings = {}
        self.docs = {}
    def add_document(self, doc_id, text):
        self.docs[doc_id] = text
        for pos, tok in enumerate(tokenize(text)):
            self.postings.setdefault(tok, {}).setdefault(doc_id, []).append(pos)
    def build_from_dir(self, root, exts=(".txt", ".md")):
        root = Path(root); n = 0
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in exts or ".git" in p.parts: continue
            try: text = p.read_text(encoding="utf-8", errors="replace")
            except OSError: continue
            self.add_document(str(p.relative_to(root)), text); n += 1
        return n
    def save(self, path):
        Path(path).write_text(json.dumps({"postings": self.postings, "docs": self.docs}, ensure_ascii=False), encoding="utf-8")
    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        idx = cls(); idx.postings = data["postings"]; idx.docs = data["docs"]; return idx
    def term_postings(self, term): return self.postings.get(term.lower(), {})
    def term_doc_ids(self, term): return set(self.term_postings(term).keys())
