import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from inverted_index.index import InvertedIndex, tokenize
from inverted_index.query import boolean_query, phrase_query

DOCS = {
    "py.txt": "python 是一门通用编程语言 python 简单易学",
    "java.txt": "java 是一门强类型编程语言 java 运行在 jvm",
    "both.txt": "python 与 java 都是面向对象语言 python 流行",
}

class TestInvertedIndex(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for n, t in DOCS.items(): (self.root / n).write_text(t, encoding="utf-8")
        self.idx = InvertedIndex()
        for n, t in DOCS.items(): self.idx.add_document(n, t)
    def tearDown(self): self.tmp.cleanup()
    def test_tokenize(self): self.assertIn("python", tokenize("Python GIL"))
    def test_postings_positions(self):
        self.assertEqual(len(self.idx.postings["python"]["py.txt"]), 2)
    def test_term_doc_ids(self):
        self.assertEqual(self.idx.term_doc_ids("python"), {"py.txt", "both.txt"})
    def test_boolean_and(self): self.assertEqual(boolean_query(self.idx, "python java"), {"both.txt"})
    def test_boolean_or(self): self.assertEqual(boolean_query(self.idx, "python | java"), {"py.txt","java.txt","both.txt"})
    def test_boolean_not(self): self.assertEqual(boolean_query(self.idx, "python -java"), {"py.txt"})
    def test_phrase_hit(self): self.assertEqual(phrase_query(self.idx, "python 与 java"), {"both.txt"})
    def test_phrase_no_hit(self): self.assertEqual(phrase_query(self.idx, "python jvm"), set())
    def test_persist_roundtrip(self):
        out = Path(self.tmp.name) / "idx.json"
        self.idx.save(out)
        idx2 = InvertedIndex.load(out)
        self.assertEqual(boolean_query(idx2, "python -java"), {"py.txt"})

if __name__ == "__main__": unittest.main()
