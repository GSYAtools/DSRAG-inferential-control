# dsrag-Inferential-Control

## Overview

This repository provides a **reproducible research framework** for validating **inferential composition control** in **federated Retrieval-Augmented Generation (RAG)** systems operating over **Data Spaces**.

It implements the experimental validation described in:

> *Engineering Inferential Composition Control for Federated RAG in Data Spaces*  
> Braga, C. M., Serrano, M. A., Fernández-Medina, E.  
> (Submitted to CIbSE 2026)

The purpose of this software is **not** to improve answer quality or normative correctness, but to **observe and constrain reasoning behavior** by controlling how retrieved fragments are composed *after retrieval and before generation*.

---

## Research Context

Federated Data Spaces integrate autonomous and semantically heterogeneous data providers.  
Standard RAG pipelines implicitly assume that all retrieved fragments can be merged into a single generation context.

In regulated domains, this may lead to **inferential collapse**, such as:
- treating ethical guidance as legally binding,
- collapsing alternative legal bases into universal requirements,
- losing conditional applicability under global queries.

This repository operationalizes **inferential composition control** by making context construction an explicit and auditable step in the RAG pipeline.

---

## Relation to Previous Work (DSRAG – IDEAL 2025)

This repository **extends and reuses** the experimental architecture introduced in:

> *Guided and Federated RAG: Architectural Models for Trustworthy AI in Data Spaces*  
> IDEAL 2025

Original repository (frozen research artifact):  
https://github.com/GSYAtools/DSRAG

Notes:
- The original DSRAG repository remains **unchanged** and frozen.
- This repository **reuses and refactors** parts of its federated RAG architecture.
- The focus here is **inferential composition**, not architectural placement of retrieval or generation.

---

## Experimental Design

The validation is a **controlled experiment** where the *same retrieval pipeline* is reused across all configurations.  
Only the **post-retrieval context construction strategy** changes.

### Context Construction Strategies

- **S1 – Baseline**  
  Standard federated RAG: all retrieved fragments are concatenated.

- **S2 – Hard Separation**  
  Fragments are grouped strictly by Data Provider.

- **S3 – Inferential Composition Control**  
  Selective separation and conservative composition based on semantic roles and local tension.

### Fixed Experimental Conditions

- **3 Data Providers**: legal, ethical, technical  
- **3 documents per provider** (9 documents total)  
- **3 queries** designed to trigger safe integration, required separation, and canonical mixing  
- Same:
  - vector indexes
  - retrieved fragments
  - language model
  - decoding parameters

This ensures that observed differences are attributable **only** to context composition.

---

## Project Structure

```
dsrag-inferential-control/
├── data/
│   ├── dp1/                  # Legal documents
│   ├── dp2/                  # Ethical documents
│   └── dp3/                  # Technical documents
│
├── indexes/
│   └── federated/            # FAISS indexes per provider
│
├── queries.py                # Fixed set of evaluation queries
│
├── run_experiment.py         # Main experiment runner (S1, S2, S3)
│
├── context_builders/
│   ├── base.py               # S1: baseline concatenation
│   ├── hard_separation.py    # S2: provider-based separation
│   └── semantic_control.py   # S3: inferential composition control
│
├── semantic/
│   ├── role_assignment.py    # Semantic role assignment
│   └── tension.py            # Local semantic tension computation
│
├── llm/
│   └── generate.py           # LLM invocation wrapper
│
├── evaluation/
│   ├── indicators.py         # Qualitative evaluation indicators
│   └── human_template.json   # Template for manual review
│
├── results/
│   └── *.json                # Contexts, prompts and responses
│
└── README.md
```

---

## How to Reproduce the Experiment

### Requirements

- Python 3.10+
- OpenAI API key

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 1. Prepare the Corpus

Place the documents in:

```
data/dp1/
data/dp2/
data/dp3/
```

Each provider should contain **three documents**.

---

### 2. Build Vector Indexes

Create FAISS indexes for each Data Provider using the indexing utilities (e.g., via `core.create_faiss_index`).  
Indexes are stored under `indexes/federated/`.

---

### 3. Run the Experiment

Execute the **single experimental runner**, which evaluates all three strategies:

```bash
python run_experiment.py
```

This script:
- runs the same retrieval pipeline for each query,
- applies S1, S2 and S3 sequentially,
- invokes the LLM with identical parameters,
- stores full traces (contexts, prompts, outputs) in `results/`.

---

## Practical Notes

- Temperature is set to **0** to ensure deterministic behavior.
- The same model instance is used across all configurations.
- Context construction is the **only experimental variable**.
- All intermediate artifacts are stored for auditability and qualitative inspection.

---

## Reproducibility Notes

This repository is designed to support:
- controlled comparison,
- reasoning traceability,
- qualitative evaluation of inferential behavior.

It is **not** intended as a production-ready RAG system.

---

## Citation and Usage

This repository is provided as a **research artifact** supporting an academic publication currently under review.

If you use or adapt this code, please cite:

> Braga, C. M., Serrano, M. A., Fernández-Medina, E.  
> *Engineering Inferential Composition Control for Federated RAG in Data Spaces*  
> CIbSE 2026 (under review)

---
