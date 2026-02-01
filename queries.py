# queries.py
# Three queries designed for the semantic-homeostasis-rag experiment.
# Q1: query that should require integration (technical + governance)
# Q2: query that should require separation (legal obligations vs ethical recommendations)
# Q3: canonical mixed question (legal + ethical + technical)

QUERIES = [
    # Q1 — Integrable (control negativo)
    "¿Qué medidas técnicas y de gobernanza deben implementarse para proteger los datos personales en proyectos de investigación?",

    # Q2 — Adversarial: colapso legal/ético
    "¿Es obligatorio cumplir simultáneamente con las obligaciones legales y las consideraciones éticas para cualquier uso de datos personales en investigación?",

    # Q3 — Adversarial: colapso de bases jurídicas
    "¿Qué requisitos deben cumplirse en todos los casos para compartir datos personales en proyectos de investigación, independientemente de la base jurídica aplicable?"
]