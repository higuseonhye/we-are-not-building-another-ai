from __future__ import annotations

from collections import Counter

from app.agents.heuristics import top_terms
from app.schemas import Comparison, Document, DocumentAnalysis


def compare_documents(documents: list[Document], analyses: list[DocumentAnalysis]) -> Comparison:
    term_sets = [set(top_terms(document.text, 12)) for document in documents]
    shared_terms = sorted(set.intersection(*term_sets)) if len(term_sets) > 1 else sorted(term_sets[0]) if term_sets else []
    all_terms = Counter(term for terms in term_sets for term in terms)
    contested_terms = [term for term, count in all_terms.items() if count == 1][:6]

    consensus = [
        f"Documents repeatedly orbit '{term}', suggesting it is a shared concept worth preserving in synthesis."
        for term in shared_terms[:5]
    ] or ["The document set does not show strong surface-level consensus; synthesis should preserve distinct viewpoints."]

    disagreements = [
        f"'{term}' appears in only one source, so it may represent a distinct perspective, blind spot, or domain-specific emphasis."
        for term in contested_terms[:5]
    ]

    hidden_assumptions = []
    for analysis in analyses:
        hidden_assumptions.extend([f"{analysis.title}: {item}" for item in analysis.assumptions[:2]])

    conflicting_logic = []
    for analysis in analyses:
        conflicting_logic.extend([f"{analysis.title}: {item}" for item in analysis.contradictions[:2]])
    if not conflicting_logic and len(documents) > 1:
        conflicting_logic.append("No explicit contradiction was detected; compare causal claims manually before deciding.")

    return Comparison(
        consensus=consensus,
        disagreements=disagreements,
        hidden_assumptions=hidden_assumptions[:6],
        conflicting_logic=conflicting_logic[:6],
    )
