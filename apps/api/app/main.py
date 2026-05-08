from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.memory.storage import JsonWorkspaceStore
from core.workflow.ingestion import ingest_upload
from core.workflow.research_loop import ResearchLoop
from core.workflow.schemas import WorkflowRun, WorkspaceState

app = FastAPI(title="Cognitive Workflow Infrastructure MVP")
store = JsonWorkspaceStore(Path(__file__).resolve().parents[1] / "data" / "workspace_memory.json")
research_loop = ResearchLoop()

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

    run = research_loop.run(readable_documents)

    state = store.load()
    state.runs.insert(0, run)
    state.memory_nodes = run.memory_nodes + state.memory_nodes
    store.save(state)
    return run
