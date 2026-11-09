#!/usr/bin/env python3
"""Rebuild the pair files from the item file and check the data.

    python scripts/build_pairs.py

Reads data/pubmed_enid_qa_500_items.csv (1,000 rows, one per pair and language; the file the
benchmark experiments read) and writes:
  data/pubmed_enid_qa_500_pairs.csv   one row per pair: question, options and answer in both languages,
                                      source abstract ID (suffix _en = English, _ind = Indonesian, ISO 639-3)
  data/pubmed_enid_qa_500_pairs.jsonl same content, one JSON object per line
  SHA256SUMS                          checksums of the three data files
It checks that every pair has an English and an Indonesian item with the same answer letter and task type,
four options A-D, and an answer text equal to the marked option. Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data/pubmed_enid_qa_500_items.csv"
EXPECTED_SHA256 = "f189b59823d3ee8d0b270db3bf975853335d213a40dc70f4a88731347333f303"
# The free Hugging Face sample (IndoHealth-NLP/PubMed-Bilingual-Medical-Sample-EN-ID) is rows 1-150 of Vol.1.
HF_SAMPLE_ROWS = 150
LETTERS = "ABCD"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_item(query: str) -> tuple[str, dict[str, str]]:
    """Question stem and the four options from the item text ('stem ... A. ... B. ... C. ... D. ...')."""
    options = dict(re.findall(r"(?m)^\s*([A-D])\.\s*(.+?)\s*$", query))
    first = re.search(r"(?m)^\s*A\.\s", query)
    stem = query[: first.start()] if first else query
    stem = re.sub(r"\n\s*(Options|Pilihan( jawaban)?)\s*:\s*$", "", stem.strip(), flags=re.I).strip()
    return stem, options


def build_pairs(rows: list[dict]) -> list[dict]:
    by_pair: dict[str, dict[str, dict]] = {}
    for r in rows:
        by_pair.setdefault(r["pair_id"], {})[r["language"]] = r
    pairs = []
    for pair_id in sorted(by_pair):
        langs = by_pair[pair_id]
        assert set(langs) == {"en", "id"}, f"{pair_id}: languages {sorted(langs)}"
        en, id_ = langs["en"], langs["id"]
        assert en["answer_index"] == id_["answer_index"] and en["task_type"] == id_["task_type"], pair_id
        docs = json.loads(en["ground_truth_docs"])
        assert docs == [pair_id], f"{pair_id}: ground_truth_docs {docs}"
        row_number = int(pair_id.rsplit("-", 1)[1])
        out = {
            "pair_id": pair_id,
            "source_document_id": pair_id,
            "vol1_row": row_number,
            "in_hf_sample": row_number <= HF_SAMPLE_ROWS,
            "task_type": en["task_type"],
            "answer": en["answer_index"],
        }
        for lang, r in (("en", en), ("ind", id_)):
            stem, options = split_item(r["query"])
            assert sorted(options) == list(LETTERS), f"{pair_id}/{lang}: options {sorted(options)}"
            assert options[r["answer_index"]] == r["ground_truth_answer"].strip(), f"{pair_id}/{lang}: answer text"
            out[f"question_{lang}"] = stem
            for letter in LETTERS:
                out[f"option_{letter.lower()}_{lang}"] = options[letter]
            out[f"answer_text_{lang}"] = options[r["answer_index"]]
        pairs.append(out)
    return pairs


def main() -> None:
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()

    items = ITEMS
    digest = sha256(items)
    if digest != EXPECTED_SHA256:
        print(f"note: {items.name} has sha256 {digest}, not the released version {EXPECTED_SHA256}")
    with items.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    pairs = build_pairs(rows)
    assert len(pairs) == 500, len(pairs)

    data = ROOT / "data"
    pairs_csv = data / "pubmed_enid_qa_500_pairs.csv"
    with pairs_csv.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(pairs[0]))
        writer.writeheader()
        writer.writerows(pairs)
    pairs_jsonl = data / "pubmed_enid_qa_500_pairs.jsonl"
    with pairs_jsonl.open("w", encoding="utf-8") as stream:
        for p in pairs:
            stream.write(json.dumps(p, ensure_ascii=False) + "\n")

    with (ROOT / "SHA256SUMS").open("w", encoding="utf-8") as stream:
        for path in (items, pairs_csv, pairs_jsonl):
            stream.write(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}\n")

    print(f"pairs: {len(pairs)}  items: {len(rows)}")
    print("task types:", dict(Counter(p["task_type"] for p in pairs)))
    print("answer letters:", dict(sorted(Counter(p["answer"] for p in pairs).items())))
    print("abstract in HF sample:", sum(p["in_hf_sample"] for p in pairs))
    print("wrote", pairs_csv, pairs_jsonl, ROOT / "SHA256SUMS", sep="\n  ")


if __name__ == "__main__":
    main()
