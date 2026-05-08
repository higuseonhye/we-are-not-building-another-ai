from __future__ import annotations

from core.reasoning.heuristics import top_terms
from core.workflow.schemas import Comparison, Document, DocumentAnalysis, Synthesis


def synthesize(documents: list[Document], analyses: list[DocumentAnalysis], comparison: Comparison) -> Synthesis:
    terms = top_terms("\n".join(document.text for document in documents), 6)
    focus = ", ".join(terms[:4]) if terms else "the uploaded material"
    claim_count = sum(len(analysis.key_claims) for analysis in analyses)
    uncertainty_count = sum(len(analysis.uncertainties) for analysis in analyses)

    summary = (
        f"The corpus centers on {focus}. Across {len(documents)} document(s), the system extracted "
        f"{claim_count} claim signals and {uncertainty_count} uncertainty signals. The strongest synthesis is not a single answer, "
        "but a working model: preserve the shared claims, isolate assumptions, and turn unresolved tensions into testable questions."
    )

    hypotheses = [
        f"If {term} is the core driver, then decisions should improve when the workflow makes its assumptions explicit."
        for term in terms[:3]
    ] or ["If assumptions are made visible before synthesis, users will make higher-confidence decisions."]

    experiment_ideas = [
        "Run a contrastive read: ask two users to make a decision with and without the comparison view, then compare confidence and blind spots.",
        "Track which generated next questions are reused in later workspaces as a proxy for durable insight.",
        "Ask users to mark one hypothesis as adopted, rejected, or unresolved after reviewing source evidence.",
    ]

    product_implications = [
        "The interface should foreground claims, assumptions, and uncertainty before presenting polished synthesis.",
        "Memory should store evolving hypotheses, not just document summaries.",
        "Comparison should make disagreements feel useful rather than adversarial.",
    ]

    next_questions = [
        "Which conclusion would change most if one assumption failed?",
        "What evidence is missing across all sources?",
        "Which disagreement is productive enough to become an experiment?",
        "What should be remembered for a future research session?",
    ]

    return Synthesis(
        summary=summary,
        hypotheses=hypotheses,
        experiment_ideas=experiment_ideas,
        product_implications=product_implications,
        next_questions=next_questions,
    )
