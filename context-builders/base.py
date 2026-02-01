"""
context_builders.base

Simple baseline context builder for S1: concatenate all retrieved fragments
in retrieval order, preserving a short provenance tag per fragment.

Functions:
- build_context_base(results): returns a single string context suitable for direct
  insertion into a prompt.
"""

def build_context_base(results):
    """
    Build the baseline context by concatenating all retrieved fragments.

    Args:
        results (list): list of objects with attributes:
                        - page_content (str)
                        - metadata (dict) with at least "dp" key

    Returns:
        str: concatenated context string
    """
    fragments = []
    for doc in results:
        dp = doc.metadata.get("dp", "unknown")
        content = doc.page_content.strip()
        fragments.append(f"[{dp}] {content}")
    return "\n\n".join(fragments)
