from __future__ import annotations

from core.synthesis.engine import synthesize
from core.workflow.schemas import Comparison, Document, DocumentAnalysis, Synthesis


class SynthesizerAgent:
    """Turns critique and comparison outputs into a working model."""

    def run(
        self,
        documents: list[Document],
        analyses: list[DocumentAnalysis],
        comparison: Comparison,
    ) -> Synthesis:
        return synthesize(documents, analyses, comparison)
