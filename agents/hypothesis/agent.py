from __future__ import annotations

from core.workflow.schemas import Synthesis


class HypothesisAgent:
    """Surfaces hypotheses as first-class objects for future memory and evaluation."""

    def run(self, synthesis: Synthesis) -> list[str]:
        return synthesis.hypotheses
