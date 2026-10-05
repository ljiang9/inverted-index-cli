"""布尔查询与短语查询。空格=AND，|=OR，-前缀=NOT。"""
from __future__ import annotations
from .index import InvertedIndex, tokenize

def boolean_query(idx, expr):
    result = set()
    for part in [p.strip() for p in expr.split("|") if p.strip()]:
        tokens = part.split()
        if not tokens: continue
        base = None; nots = []
        for t in tokens:
            if t.startswith("-") and len(t) > 1:
                nots.append(idx.term_doc_ids(t[1:])); continue
            ids = idx.term_doc_ids(t)
            base = ids if base is None else (base & ids)
        if base is None: base = set()
        for n in nots: base = base - n
        result |= base
    return result

def phrase_query(idx, phrase):
    toks = tokenize(phrase)
    if not toks: return set()
    candidates = None
    for t in toks:
        ids = set(idx.term_postings(t).keys())
        candidates = ids if candidates is None else (candidates & ids)
    if not candidates: return set()
    out = set()
    for doc in candidates:
        for p in idx.postings[toks[0]][doc]:
            if all(p + i in idx.postings[t].get(doc, []) for i, t in enumerate(toks)):
                out.add(doc); break
    return out
