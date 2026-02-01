"""
context_builders.hard_separation

Hard separation context builder for S2: group fragments strictly by Data Provider (DP).
Each DP appears as an explicit labeled block. The model receives a single prompt
where blocks are separated and labeled, discouraging cross-block accumulation.

Functions:
- build_context_hard(results): returns a single string context with DP blocks.
"""

from collections import defaultdict

def build_context_hard(results):
    """
    Build a context that groups fragments by their data provider.

    Args:
        results (list): list of objects with attributes:
                        - page_content (str)
                        - metadata (dict) with at least "dp" key

    Returns:
        str: structured context string with one block per DP
    """
    grouped = defaultdict(list)
    for doc in results:
        dp = doc.metadata.get("dp", "unknown")
        content = doc.page_content.strip()
        grouped[dp].append(content)

    blocks = []
    for dp, docs in grouped.items():
        header = f"=== Fragments from {dp} ==="
        block = header + "\n\n" + "\n\n".join(docs)
        blocks.append(block)

    return "\n\n".join(blocks)
