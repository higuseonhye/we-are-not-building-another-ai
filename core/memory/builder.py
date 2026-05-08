from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from core.workflow.schemas import MemoryNode, Synthesis


def build_memory_nodes(synthesis: Synthesis, run_id: str) -> list[MemoryNode]:
    nodes: list[MemoryNode] = []
    for hypothesis in synthesis.hypotheses:
        nodes.append(
            MemoryNode(
                id=str(uuid4()),
                kind="hypothesis",
                label=hypothesis[:96],
                detail=hypothesis,
                links=[run_id],
                created_at=datetime.now(timezone.utc),
            )
        )

    for question in synthesis.next_questions[:2]:
        nodes.append(
            MemoryNode(
                id=str(uuid4()),
                kind="question",
                label=question[:96],
                detail=question,
                links=[run_id],
                created_at=datetime.now(timezone.utc),
            )
        )

    return nodes
