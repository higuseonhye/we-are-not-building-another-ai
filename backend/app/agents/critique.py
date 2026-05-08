from __future__ import annotations

from app.agents.heuristics import (
    ASSUMPTION_MARKERS,
    CLAIM_MARKERS,
    CONTRADICTION_MARKERS,
    UNCERTAINTY_MARKERS,
    WEAKNESS_MARKERS,
    fallback_list,
    pick_sentences,
    top_terms,
)
from app.schemas import Document, DocumentAnalysis


def analyze_document(document: Document) -> DocumentAnalysis:
    terms = top_terms(document.text)
    key_claims = pick_sentences(document.text, CLAIM_MARKERS, 5) or fallback_list("Claim candidate:", terms, 3)
    assumptions = pick_sentences(document.text, ASSUMPTION_MARKERS, 4) or fallback_list("Assumption to test:", terms[1:], 3)
    weak_points = pick_sentences(document.text, WEAKNESS_MARKERS, 4) or [
        "Evidence quality, scope, and omitted counterexamples should be checked before relying on this document."
    ]
    uncertainties = pick_sentences(document.text, UNCERTAINTY_MARKERS, 4) or [
        "The confidence level is not explicit; identify what would change this conclusion."
    ]
    contradictions = pick_sentences(document.text, CONTRADICTION_MARKERS, 4)
    alternative_framings = [
        f"Frame this through the lens of {term}: what changes if that is the primary variable?"
        for term in terms[:4]
    ]

    return DocumentAnalysis(
        document_id=document.id,
        title=document.title,
        key_claims=key_claims,
        assumptions=assumptions,
        weak_points=weak_points,
        uncertainties=uncertainties,
        contradictions=contradictions,
        alternative_framings=alternative_framings,
    )
