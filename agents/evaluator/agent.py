from __future__ import annotations

from core.workflow.schemas import WorkflowRun


class EvaluatorAgent:
    """Evaluates whether a workflow run preserved uncertainty and reasoning depth."""

    def run(self, workflow_run: WorkflowRun) -> dict[str, int]:
        return {
            "documents": len(workflow_run.documents),
            "claims": sum(len(analysis.key_claims) for analysis in workflow_run.analyses),
            "uncertainties": sum(len(analysis.uncertainties) for analysis in workflow_run.analyses),
            "hypotheses": len(workflow_run.synthesis.hypotheses),
            "memory_nodes": len(workflow_run.memory_nodes),
        }
