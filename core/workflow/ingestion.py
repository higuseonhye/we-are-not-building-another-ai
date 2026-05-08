from __future__ import annotations

import io
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from core.workflow.schemas import Document


async def ingest_upload(file: UploadFile) -> Document:
    raw = await file.read()
    suffix = Path(file.filename or "document.txt").suffix.lower()
    title = Path(file.filename or "Untitled document").stem

    if suffix == ".pdf":
        text = extract_pdf_text(raw)
        source_type = "pdf"
    else:
        text = raw.decode("utf-8", errors="ignore")
        source_type = suffix.replace(".", "") or "text"

    return Document(
        id=str(uuid4()),
        title=title,
        source_type=source_type,
        text=normalize_text(text),
        created_at=datetime.now(timezone.utc),
    )


def extract_pdf_text(raw: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""

    reader = PdfReader(io.BytesIO(raw))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def normalize_text(text: str) -> str:
    lines = [line.strip() for line in text.replace("\r", "\n").split("\n")]
    compact = [line for line in lines if line]
    return "\n".join(compact)
