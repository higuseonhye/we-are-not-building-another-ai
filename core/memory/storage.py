from __future__ import annotations

import json
from pathlib import Path

from core.workflow.schemas import WorkspaceState


class JsonWorkspaceStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> WorkspaceState:
        if not self.path.exists():
            return WorkspaceState()

        with self.path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return WorkspaceState.model_validate(payload)

    def save(self, state: WorkspaceState) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(state.model_dump(mode="json"), handle, indent=2)
