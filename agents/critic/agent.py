from __future__ import annotations

from core.critique.engine import analyze_document
from core.workflow.schemas import Document, DocumentAnalysis


class CriticAgent:
    """Extracts claims, assumptions, uncertainty, and weak points."""

    def run(self, document: Document) -> DocumentAnalysis:
        return analyze_document(document)
