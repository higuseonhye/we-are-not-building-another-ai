from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.agents.comparison import compare_documents
from app.agents.critique import analyze_document
from app.agents.memory import build_memory_nodes
from app.agents.synthesis import synthesize
from app.ingestion import ingest_upload
from app.schemas import WorkflowRun, WorkspaceState
from app.storage import JsonWorkspaceStore

app = FastAPI(title="Cognitive Workflow Infrastructure MVP")
store = JsonWorkspaceStore(Path(__file__).resolve().parents[1] / "data" / "workspace_memory.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):30[0-9]{2}",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/workspace", response_model=WorkspaceState)
def workspace() -> WorkspaceState:
    return store.load()


@app.post("/workflows/analyze", response_model=WorkflowRun)
async def analyze(files: list[UploadFile] = File(...)) -> WorkflowRun:
    if not files:
        raise HTTPException(status_code=400, detail="Upload at least one document.")

    documents = [await ingest_upload(file) for file in files]
    readable_documents = [document for document in documents if document.text.strip()]
    if not readable_documents:
        raise HTTPException(status_code=400, detail="No readable text was found in the uploaded files.")

    analyses = [analyze_document(document) for document in readable_documents]
    comparison = compare_documents(readable_documents, analyses)
    synthesis = synthesize(readable_documents, analyses, comparison)

    run_id = str(uuid4())
    memory_nodes = build_memory_nodes(synthesis, run_id)
    run = WorkflowRun(
        id=run_id,
        created_at=datetime.now(timezone.utc),
        documents=readable_documents,
        analyses=analyses,
        comparison=comparison,
        synthesis=synthesis,
        memory_nodes=memory_nodes,
    )

    state = store.load()
    state.runs.insert(0, run)
    state.memory_nodes = memory_nodes + state.memory_nodes
    store.save(state)
    return run
