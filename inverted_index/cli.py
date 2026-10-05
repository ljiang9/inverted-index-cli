"""命令行入口：build / query / phrase。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .index import InvertedIndex
from .query import boolean_query, phrase_query


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="inv-idx", description="倒排索引构建/查询")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pb = sub.add_parser("build", help="对目录建索引")
    pb.add_argument("dir"); pb.add_argument("--out", default="index.json")
    pb.set_defaults(func=_build)
    pq = sub.add_parser("query", help="布尔查询：a b | c -d")
    pq.add_argument("expr"); pq.add_argument("--index", default="index.json")
    pq.set_defaults(func=_query)
    pp = sub.add_parser("phrase", help="短语查询（要求相邻出现）")
    pp.add_argument("phrase"); pp.add_argument("--index", default="index.json")
    pp.set_defaults(func=_phrase)
    args = ap.parse_args(argv)
    return args.func(args)


def _load(p):
    if not Path(p).exists():
        print(f"索引不存在: {p}（请先 build）", file=sys.stderr); sys.exit(2)
    return InvertedIndex.load(p)


def _build(args):
    if not Path(args.dir).is_dir():
        print(f"目录不存在: {args.dir}", file=sys.stderr); return 2
    idx = InvertedIndex()
    n = idx.build_from_dir(args.dir)
    idx.save(args.out)
    print(f"已索引 {n} 个文档，{len(idx.postings)} 个 term -> {args.out}")
    return 0


def _query(args):
    idx = _load(Path(args.index))
    hits = boolean_query(idx, args.expr)
    print(f"命中 {len(hits)} 个文档：")
    for d in sorted(hits): print(f"  - {d}")
    return 0


def _phrase(args):
    idx = _load(Path(args.index))
    hits = phrase_query(idx, args.phrase)
    print(f"短语 {args.phrase} 命中 {len(hits)} 个文档：")
    for d in sorted(hits): print(f"  - {d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
