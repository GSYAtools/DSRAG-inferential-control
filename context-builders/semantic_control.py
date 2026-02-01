"""
context_builders.semantic_control

Selective semantic control context builder for S3.
Implements:
- role assignment via lightweight linguistic cues
- ordinal semantic tension (low/medium/high)
- selective separation for high local tension
- conservative composition for transversal descriptive fragments

This module intentionally avoids ML training and ontologies. All rules are
deterministic and reproducible.
"""

from collections import defaultdict

# --- Role assignment ---------------------------------------------------------

ROLE_KEYWORDS = {
    "normative": ["debe", "deberá", "obligatorio", "requiere", "está obligado", "no puede"],
    "alternative": ["o bien", "alternativamente", "excepto", "en su defecto"],
    "orientative": ["se recomienda", "debería", "es aconsejable", "buena práctica"],
}

def assign_roles(text):
    """
    Assign one or more semantic roles to a fragment based on lightweight cues.

    Args:
        text (str): fragment text

    Returns:
        set[str]: roles in {"descriptive","normative","alternative","orientative"}
    """
    t = text.lower()
    roles = set()

    for role, kws in ROLE_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                roles.add(role)
                break

    if not roles:
        roles.add("descriptive")

    return roles


# --- Semantic tension --------------------------------------------------------

# Ordinal role incompatibility matrix
ROLE_TENSION = {
    ("descriptive","descriptive"): "low",
    ("descriptive","normative"): "medium",
    ("descriptive","alternative"): "medium",
    ("descriptive","orientative"): "low",

    ("normative","descriptive"): "medium",
    ("normative","normative"): "high",
    ("normative","alternative"): "high",
    ("normative","orientative"): "medium",

    ("alternative","descriptive"): "medium",
    ("alternative","normative"): "high",
    ("alternative","alternative"): "medium",
    ("alternative","orientative"): "medium",

    ("orientative","descriptive"): "low",
    ("orientative","normative"): "medium",
    ("orientative","alternative"): "medium",
    ("orientative","orientative"): "low",
}

LEVELS = ["low", "medium", "high"]

def increase(level):
    """Increase ordinal tension by one step."""
    i = LEVELS.index(level)
    return LEVELS[min(i + 1, len(LEVELS) - 1)]

def pair_tension(roles_a, roles_b, dp_a, dp_b, text_a, text_b):
    """
    Compute ordinal tension for a pair of fragments.

    Increases tension when:
    - fragments come from different DPs
    - both contain deontic language

    Returns:
        str: "low" | "medium" | "high"
    """
    # base from role pairs (max over combinations)
    base = "low"
    for ra in roles_a:
        for rb in roles_b:
            base = LEVELS[max(LEVELS.index(base), LEVELS.index(ROLE_TENSION[(ra, rb)]))]

    # increase if different providers
    if dp_a != dp_b:
        base = increase(base)

    # increase if both contain deontic cues
    deontic = any(k in text_a.lower() for k in ROLE_KEYWORDS["normative"]) and               any(k in text_b.lower() for k in ROLE_KEYWORDS["normative"])
    if deontic:
        base = increase(base)

    return base


# --- Context builder ---------------------------------------------------------

def build_context_semantic(results, query=None):
    """
    Build a structured context applying selective separation and conservative composition.

    Args:
        results (list): list of docs with attributes:
                        - page_content (str)
                        - metadata (dict) with "dp"
        query (str): original query (unused for now, kept for extensibility)

    Returns:
        str: structured context string
    """
    # Prepare fragments
    frags = []
    for doc in results:
        frags.append({
            "text": doc.page_content.strip(),
            "dp": doc.metadata.get("dp", "unknown"),
            "roles": assign_roles(doc.page_content),
        })

    # Compute local tensions
    n = len(frags)
    high_conflict = set()  # indices participating in high tension
    for i in range(n):
        for j in range(i + 1, n):
            t = pair_tension(
                frags[i]["roles"], frags[j]["roles"],
                frags[i]["dp"], frags[j]["dp"],
                frags[i]["text"], frags[j]["text"]
            )
            if t == "high":
                high_conflict.add(i)
                high_conflict.add(j)

    # Conservative composition rules
    integrated = []
    separated = defaultdict(list)

    # Count transversal occurrences (simple heuristic)
    counts = defaultdict(int)
    for f in frags:
        if "descriptive" in f["roles"]:
            counts[f["text"]] += 1

    for idx, f in enumerate(frags):
        # integrate only descriptive fragments that are transversal and conflict-free
        if (
            "descriptive" in f["roles"]
            and counts[f["text"]] >= 2
            and idx not in high_conflict
            and "normative" not in f["roles"]
        ):
            integrated.append(f["text"])
        else:
            separated[(f["dp"], tuple(sorted(f["roles"])))].append(f["text"])

    # Render structured context
    blocks = []

    if integrated:
        blocks.append(
            "=== Contexto común (integrado) ===\n" +
            "\n\n".join(integrated)
        )

    for (dp, roles), texts in separated.items():
        role_label = ", ".join(roles)
        header = f"=== {dp} ({role_label}) ==="
        blocks.append(header + "\n" + "\n\n".join(texts))

    return "\n\n".join(blocks)
