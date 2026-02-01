# dsrag-Inferential-Control

## Overview

This repository provides a **reproducible research framework** for studying **inferential composition control** in **federated Retrieval-Augmented Generation (RAG)** systems operating over **Data Spaces**.

The software implements and validates the approach presented in:

> *Engineering Inferential Composition Control for Federated RAG in Data Spaces*  
> Braga, C. M., Serrano, M. A., Fernández-Medina, E.  
> (Submitted to CIbSE 2026)

The goal of this repository is **not** to improve answer fluency or accuracy, but to **control how retrieved fragments are composed before generation**, in order to prevent **inferential collapse** in regulated and heterogeneous environments.

---

## Research Context

Federated Data Spaces integrate autonomous and semantically heterogeneous data providers.  
While Retrieval-Augmented Generation (RAG) improves grounding and traceability, standard RAG pipelines implicitly assume that all retrieved fragments can be safely merged into a single generation context.

In regulated domains, this assumption may lead to **invalid inferences**, such as:
- treating ethical recommendations as legally binding obligations,
- collapsing alternative legal bases into universal requirements,
- masking conditional applicability under global prompts.

This repository operationalizes **inferential composition control** by explicitly structuring the generation context **before** invoking the language model.

---

## Relation to Previous Work (DSRAG – IDEAL 2025)

This repository **extends and reuses** the experimental framework introduced in:

> *Guided and Federated RAG: Architectural Models for Trustworthy AI in Data Spaces*  
> IDEAL 2025

The original framework is available at:  
https://github.com/GSYAtools/DSRAG

**Important notes:**
- The original DSRAG repository is **kept frozen** as a research artifact associated with the IDEAL 2025 paper.
- This repository **does not modify** the original artifact.
- Selected components of the DSRAG architecture are **copied and refactored** to support inferential composition control.

In short:

> **DSRAG (IDEAL 2025)** evaluates *where* retrieval and generation occur.  
> **This repository (CIbSE 2026)** evaluates *how* retrieved information is composed for reasoning.

---

## What This Repository Provides

- A modular implementation of **three context construction strategies**:
  - **Baseline**: standard RAG context concatenation
  - **Hard Separation**: provider-based grouping without inferential control
  - **Inferential Control**: role-aware, tension-based context construction
- A reproducible experimental setup using:
  - the same corpus,
  - the same queries,
  - the same retrieval results,
  across all configurations
- Scripts and artifacts to **observe and compare reasoning behavior**, rather than optimize model output.

---

## Project Structure

```
dsrag-inferential-control/
├── context_builders/
│   ├── base.py               # Baseline RAG: direct fragment concatenation
│   ├── hard_separation.py    # Grouping by Data Provider (DP)
│   └── semantic_control.py   # Inferential composition control
│
├── core.py                   # Shared utilities (document loading, indexing, retrieval)
├── evaluation/
│   └── indicators.py         # Qualitative indicators used in analysis
│
├── data/
│   ├── dp1/                  # Legal data provider corpus
│   ├── dp2/                  # Ethical data provider corpus
│   └── dp3/                  # Technical data provider corpus
│
├── indexes/                  # Vector indexes per provider
├── results/
│   └── results_semantic_homeostasis.json
│
└── README.md
```

---

## Context Construction Strategies

### Baseline (Standard RAG)

All retrieved fragments are concatenated into a single context with minimal provenance tagging.
This configuration represents **standard RAG behavior**.

### Hard Separation

Retrieved fragments are grouped by Data Provider.  
Provenance is preserved, but inferential interactions are not explicitly controlled.

### Inferential Composition Control

Fragments are assigned lightweight **semantic roles** and combined using **selective separation**
and **conservative composition** to prevent inferential collapse.

---

## How to Run the Experiments

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

### Corpus

The repository includes a ready-to-use corpus under `data/`, organized by Data Provider.

### Indexing

Build vector indexes per provider:

```bash
python core.py
```

### Execution

Select the desired context builder in the experiment script:

- `base.py` → baseline
- `hard_separation.py` → hard separation
- `semantic_control.py` → inferential control

Each run produces structured outputs under `results/`.

---

## Reproducibility Notes

- All configurations use the same corpus, queries, and retrieval results.
- Differences in outputs are attributable **only** to context construction strategy.
- Deterministic decoding is recommended to reproduce the results reported in the paper.

---

## Citation and Usage

This repository is provided as a **research artifact** supporting an academic publication currently under review.

If you use or adapt this code, please cite:

> Braga, C. M., Serrano, M. A., Fernández-Medina, E.  
> *Engineering Inferential Composition Control for Federated RAG in Data Spaces*  
> CIbSE 2026 (under review)

---
