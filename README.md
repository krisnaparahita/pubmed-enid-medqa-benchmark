# PubMed EN-ID Medical QA Benchmark (500 pairs)

A bilingual **English–Indonesian** multiple-choice question set for testing medical
language models. It has **500 question pairs** (1,000 items). Each pair is one question,
with four options and one correct answer, written in both English and Indonesian. Every
pair is based on one source abstract from *The PubMed Bilingual Medical Corpus (EN-ID):
Volume 1* by IndoHealth-NLP (free sample on Hugging Face:
[IndoHealth-NLP/PubMed-Bilingual-Medical-Sample-EN-ID](https://huggingface.co/datasets/IndoHealth-NLP/PubMed-Bilingual-Medical-Sample-EN-ID)).
All 500 pairs were checked one by one against their source abstract
(see [VALIDATION.md](VALIDATION.md)).

The set was built for the thesis *Combating Clinical Hallucinations Across Languages: A
Multilingual Benchmark of RAG Architectures for Open-Weight Medical LLMs in English and
Bahasa Indonesia*.

> **Not for clinical use.** This is a research benchmark. It is not a source of medical
> advice and must not be used for patient care.

## At a glance

| | |
|---|---|
| Pairs / items | 500 pairs = 1,000 items (500 English + 500 Indonesian) |
| Format | Multiple choice, four options (A–D), exactly one correct |
| Task types | Diagnostic reasoning 169 · Triage / referral 169 · Medication / dosage 162 |
| Answer key | A 125 · B 125 · C 125 · D 125. The same letter is correct in both languages |
| Source | One abstract per pair, from The PubMed Bilingual Medical Corpus (EN-ID): Volume 1 (IndoHealth-NLP) |
| Review | 500 of 500 pairs checked against the abstract; 2 wrong keys corrected; 0 open issues |
| Licence | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (see [Licence](#licence)) |

## Folder contents

```text
├── README.md                          this file
├── VALIDATION.md                      the reviewer's verification and validation report
├── LICENSE                            full text of the CC BY-NC 4.0 licence
├── CITATION.cff                       citation metadata
├── SHA256SUMS                         checksums of the data files
├── scripts/build_pairs.py             rebuilds the pair files from the item file and checks the data
└── data/
    ├── pubmed_enid_qa_500_pairs.csv   one row per pair, both languages side by side (easiest to read)
    ├── pubmed_enid_qa_500_pairs.jsonl same as the CSV, one JSON object per line
    └── pubmed_enid_qa_500_items.csv   one row per item, the format used in the thesis experiments
```

All files are UTF-8. The three data files hold the same 500 pairs in different layouts.

### `pubmed_enid_qa_500_pairs.csv` / `.jsonl` (one row per pair)

| Column | Meaning |
|---|---|
| `pair_id` | Pair identifier, e.g. `pubmed-enid-00001` |
| `source_document_id` | Identifier of the source abstract in the corpus (same value as `pair_id`) |
| `vol1_row` | Row number of the source abstract in the corpus file `PubMed_Bilingual_Medical_Corpus_EN_ID_Vol_1.csv` (1-based, header not counted) |
| `in_hf_sample` | `True` if the abstract is in the free Hugging Face sample (Vol.1 rows 1–150) |
| `task_type` | `diagnostic_reasoning`, `triage_referral` or `medication_dosage` |
| `answer` | Correct option letter (`A`–`D`), the same for both languages |
| `question_en`, `option_a_en` … `option_d_en`, `answer_text_en` | English question, the four options and the text of the correct option |
| `question_ind`, `option_a_ind` … `option_d_ind`, `answer_text_ind` | The same in Indonesian. The suffix is `_ind` (ISO 639-3) so that it is not read as "ID" |

### `pubmed_enid_qa_500_items.csv` (one row per item)

This is the file used in the thesis experiments, unchanged (sha256 `f189b598…f303`).

| Column | Meaning |
|---|---|
| `item_id` | `<pair_id>-en` or `<pair_id>-id` |
| `language` | `en` or `id` |
| `pair_id` | Links the English and Indonesian item of the same pair |
| `task_type` | As above |
| `query` | The full prompt text: question, then `Options:`, then the four options on lines `A.` – `D.` |
| `ground_truth_answer` | Text of the correct option |
| `ground_truth_docs` | JSON list with the source abstract ID, e.g. `["pubmed-enid-00001"]`. Used to score retrieval |
| `requires_refusal` | Always `False` (every question can be answered from its abstract) |
| `answer_index` | Correct option letter (`A`–`D`) |

### Example (pair `pubmed-enid-00001`, task type `triage_referral`, answer **D**)

| | English | Indonesian |
|---|---|---|
| Question | In this study of odontogenic infections, which conditions were the strongest predictors of prolonged hospital length of stay? | Dalam studi infeksi odontogenik ini, kondisi manakah yang merupakan prediktor terkuat lama rawat inap yang berkepanjangan? |
| A | Maxillary sinusitis and periodontal abscess formation | Sinusitis maksilaris dan pembentukan abses periodontal |
| B | Dry socket and gingival abscess | Osteitis alveolar dan abses gingiva |
| C | Periapical abscess and pericoronitis | Abses periapikal dan perikoronitis |
| **D** | **Necrotizing fasciitis and Ludwig's angina** | **Fasiitis nekrotikans dan angina Ludwig** |

## Source abstracts

The abstracts are **not** included in this folder. They belong to the source corpus and
are referenced by ID only. To read the abstract behind a question:

1. **Free sample (21 of the 500 pairs).** The Hugging Face dataset
   [IndoHealth-NLP/PubMed-Bilingual-Medical-Sample-EN-ID](https://huggingface.co/datasets/IndoHealth-NLP/PubMed-Bilingual-Medical-Sample-EN-ID)
   holds rows 1–150 of Vol.1, in the same order. For pairs with `in_hf_sample = True`, the
   abstract is row `vol1_row` of the sample file
   `PubMed_Bilingual_Medical_Corpus_EN_ID_Sample_150.csv`.
2. **Full corpus (all 500 pairs).** The other 479 abstracts are in the full
   *PubMed Bilingual Medical Corpus EN-ID, Volume 1* (4,996 abstract pairs), which
   IndoHealth-NLP distributes. The Hugging Face page links to it. The abstract
   for a pair is row `vol1_row` of `PubMed_Bilingual_Medical_Corpus_EN_ID_Vol_1.csv`.

Each corpus row has an English text (`Inggris_Ringkasan`) and its Indonesian translation
(`Indonesia_Terjemahan`). According to IndoHealth-NLP, the English text is a summary of a
full-text PubMed Central article, written by a Gemini model, and the Indonesian text is a
Gemini medical translation of it. This README and VALIDATION.md call these texts
"abstracts" for short; they are not the abstracts as published in PubMed. The English question was written from the English
abstract. The Indonesian question is checked against the English question (criterion Z
in [VALIDATION.md](VALIDATION.md)).

```python
import pandas as pd

pairs = pd.read_csv("data/pubmed_enid_qa_500_pairs.csv")
corpus = pd.read_csv("PubMed_Bilingual_Medical_Corpus_EN_ID_Vol_1.csv")  # or the 150-row sample
corpus["vol1_row"] = range(1, len(corpus) + 1)
merged = pairs.merge(corpus, on="vol1_row", how="left")
```

## How the set was made

1. **Source selection.** Abstracts were sampled from Vol.1, and each was given a
   target task type (diagnostic reasoning, triage / referral, or medication / dosage). This
   assignment sets which kind of question to write; it does not classify the abstract.
2. **Question writing.** A large language model (Claude Opus 4.8, 20 August 2026) wrote
   one question per abstract in English and Indonesian, with four options. The question
   has to be answerable from the abstract alone. Every pair passed automatic structural
   checks (four options, one marked answer, matching English and Indonesian items).
3. **Option rewrite and balancing.** The wrong options were rewritten to be specific,
   plausible and about as long as the correct option, so that the longest option is no
   longer a hint. The position of the correct answer was then shuffled the same way in
   both languages, giving 125 correct answers per letter.
4. **Review.** The corpus reviewer (Moh. Nafik, S.Kep, IndoHealth-NLP) checked every pair
   against its abstract on seven criteria, with an independent model auditor. Two answer
   keys were wrong and were corrected; the corrected pairs passed a re-audit. Full details
   are in [VALIDATION.md](VALIDATION.md).

To check the files, and to rebuild the pair files from the item file (Python 3, standard
library only):

```bash
shasum -a 256 -c SHA256SUMS        # or: sha256sum -c SHA256SUMS
python scripts/build_pairs.py
```

## Using the benchmark

- **Without retrieval.** Give the model `query` (or the question and options from the
  pairs file) and compare its chosen letter with `answer` / `answer_index`. Report
  English and Indonesian separately; the pairing lets you compare the same question
  across the two languages.
- **With retrieval (RAG).** Index the Vol.1 abstracts with `document_id = pubmed-enid-NNNNN`
  (`NNNNN` = `vol1_row`, five digits). `ground_truth_docs` then tells you whether the
  retriever found the right abstract (precision@k, recall@k, MRR, nDCG).

## Limits

- The questions were written by a language model from abstracts, not by clinicians. The
  review checked that each one matches its abstract and is clinically reasonable. It is
  not a clinical guideline.
- Each answer is correct **according to its abstract**, which reports one study. It may
  not hold for other populations or in later evidence. Review was against the abstract,
  not the full article.
- Each question asks about the findings of one specific study, so it may not be
  answerable without the abstract. Scores without retrieval measure what a model already
  knows about those findings, not general clinical skill.
- Indonesian items are translations of the English items, checked for faithfulness. They
  were not written separately by Indonesian clinicians.
- The source texts are model-written summaries of the articles (see "Source abstracts").
  A question is only as accurate as the summary it was written from.
- Every question has an answer in its abstract (`requires_refusal` is always `False`),
  so the set does not test when a model should decline to answer.

## Licence

The questions, answer options and answer keys are licensed under the
[Creative Commons Attribution-NonCommercial 4.0 International licence (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/),
as agreed with the source corpus author (IndoHealth-NLP). The full text is in
[LICENSE](LICENSE). You may share and adapt the data for non-commercial purposes if you
give credit (see [Citation](#citation)) and say whether you made changes. Commercial use
needs a separate written agreement with the authors.

The licence covers this question set only. The source abstracts are not included and
remain under the terms of *The PubMed Bilingual Medical Corpus (EN-ID): Volume 1*
(IndoHealth-NLP).

## Citation

If you use this benchmark, please cite it and credit the source corpus as
**IndoHealth-NLP, The PubMed Bilingual Medical Corpus (EN-ID): Volume 1 (4,996 pairs)**:

```bibtex
@misc{diwakara2026pubmedenidqa,
  title        = {PubMed EN-ID Medical QA Benchmark (500 pairs)},
  author       = {Diwakara, Mohammad Krisna Parahita and Nafik, Moh.},
  year         = {2026},
  howpublished = {\url{https://github.com/krisnaparahita/pubmed-enid-medqa-benchmark}},
  note         = {Bilingual English-Indonesian multiple-choice questions built from The PubMed Bilingual Medical Corpus (EN-ID): Volume 1; reviewed by IndoHealth-NLP}
}

@misc{indohealthnlp_pubmed_enid_vol1,
  title        = {The PubMed Bilingual Medical Corpus (EN-ID): Volume 1 (4,996 pairs)},
  author       = {{IndoHealth-NLP}},
  note         = {Free 150-pair sample: Hugging Face, doi:10.57967/hf/9675},
  howpublished = {\url{https://huggingface.co/datasets/IndoHealth-NLP/PubMed-Bilingual-Medical-Sample-EN-ID}}
}
```

## Acknowledgements and contact

- Source corpus and review: IndoHealth-NLP; reviewer Moh. Nafik, S.Kep.
- Question set and benchmark code: Mohammad Krisna Parahita Diwakara.

Please report errors in a question or answer key through an issue in this repository,
with the `pair_id`.
