from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from agents.critic import CriticAgent
from agents.synthesizer import SynthesizerAgent
from core.comparison.engine import compare_documents
from core.memory.builder import build_memory_nodes
from core.workflow.schemas import Document, WorkflowRun


class ResearchLoop:
    """Research -> Critique -> Comparison -> Synthesis -> Hypothesis."""

    def __init__(self) -> None:
        self.critic = CriticAgent()
        self.synthesizer = SynthesizerAgent()

    def run(self, documents: list[Document]) -> WorkflowRun:
        analyses = [self.critic.run(document) for document in documents]
        comparison = compare_documents(documents, analyses)
        synthesis = self.synthesizer.run(documents, analyses, comparison)

        run_id = str(uuid4())
        memory_nodes = build_memory_nodes(synthesis, run_id)
        return WorkflowRun(
            id=run_id,
            created_at=datetime.now(timezone.utc),
            documents=documents,
            analyses=analyses,
            comparison=comparison,
            synthesis=synthesis,
            memory_nodes=memory_nodes,
        )
