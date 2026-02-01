"""
run_experiment.py

Runs the semantic-homeostasis-rag experiment.
For each query:
- performs federated retrieval once
- builds three contexts (S1, S2, S3)
- calls the same LLM three times (temperature=0)
- measures per-system latency
- stores contexts and responses for comparison
"""

import os
import time
import json

from core import load_documents, create_faiss_index, query_index
from queries import QUERIES

from context_builders.base import build_context_base
from context_builders.hard_separation import build_context_hard
from context_builders.semantic_control import build_context_semantic

from langchain.chat_models import ChatOpenAI

# --- Configuration -----------------------------------------------------------

DPS = ["data/dp1", "data/dp2", "data/dp3"]
INDEX_BASE = "indexes/federated"
RESULTS_FILE = "results/results_semantic_homeostasis.json"
MODEL_NAME = "gpt-4"
TEMPERATURE = 0

# --- Helpers ----------------------------------------------------------------

def ensure_indexes():
    os.makedirs(INDEX_BASE, exist_ok=True)
    for dp_path in DPS:
        dp_name = os.path.basename(dp_path)
        index_path = os.path.join(INDEX_BASE, dp_name)
        os.makedirs(index_path, exist_ok=True)
        docs = load_documents([dp_path])
        create_faiss_index(docs, index_path)

def federated_retrieve(query):
    all_results = []
    for dp_path in DPS:
        dp_name = os.path.basename(dp_path)
        index_path = os.path.join(INDEX_BASE, dp_name)
        dp_results = query_index(index_path, query)
        all_results.extend(dp_results)
    return all_results

def render_prompt(context, query):
    return (
        "Answer the following question based only on the context below.\n\n"
        "If the context presents different types of information or perspectives, "
        "make them explicit in your answer and avoid introducing unstated assumptions.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )


# --- Main -------------------------------------------------------------------

def main():
    os.makedirs("results", exist_ok=True)
    ensure_indexes()

    llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

    experiment_log = []

    for qi, query in enumerate(QUERIES, start=1):
        print(f"\n[Query {qi}] {query}")

        # Shared retrieval
        retrieval_start = time.time()
        results = federated_retrieve(query)
        retrieval_end = time.time()

        # Build contexts
        contexts = {
            "S1_base": build_context_base(results),
            "S2_hard": build_context_hard(results),
            "S3_semantic": build_context_semantic(results, query),
        }

        # LLM calls with per-system timing
        responses = {}
        timings_ms = {}

        for system_name, ctx in contexts.items():
            prompt = render_prompt(ctx, query)
            t0 = time.time()
            responses[system_name] = llm.predict(prompt)
            t1 = time.time()
            timings_ms[system_name] = round((t1 - t0) * 1000, 2)

        entry = {
            "query_index": qi,
            "query": query,
            "retrieved_fragments": len(results),
            "retrieval_latency_ms": round((retrieval_end - retrieval_start) * 1000, 2),
            "generation_latency_ms": timings_ms,
            "contexts_preview": {k: v[:1000] for k, v in contexts.items()},
            "responses": responses,
        }

        experiment_log.append(entry)

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(experiment_log, f, indent=2, ensure_ascii=False)

    print(f"\n[Done] Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
