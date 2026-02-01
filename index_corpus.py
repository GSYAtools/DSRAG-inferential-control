"""
index_corpus.py

Builds one FAISS index per Data Provider (DP) for the
semantic-homeostasis-rag experiment.

This script should be executed once before running the experiment.
"""

import os
from core import load_documents, create_faiss_index

DPS = ["data/dp1", "data/dp2", "data/dp3"]
INDEX_BASE = "indexes/federated"

def main():
    os.makedirs(INDEX_BASE, exist_ok=True)

    for dp_path in DPS:
        dp_name = os.path.basename(dp_path)
        index_path = os.path.join(INDEX_BASE, dp_name)
        os.makedirs(index_path, exist_ok=True)

        print(f"[Indexing] {dp_name}")
        docs = load_documents([dp_path])
        create_faiss_index(docs, index_path)

    print("[Done] All DP indexes created.")

if __name__ == "__main__":
    main()
