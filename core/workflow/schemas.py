from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    title: str
    source_type: str
    text: str
    created_at: datetime


class DocumentAnalysis(BaseModel):
    document_id: str
    title: str
    key_claims: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    weak_points: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    alternative_framings: List[str] = Field(default_factory=list)


class Comparison(BaseModel):
    consensus: List[str] = Field(default_factory=list)
    disagreements: List[str] = Field(default_factory=list)
    hidden_assumptions: List[str] = Field(default_factory=list)
    conflicting_logic: List[str] = Field(default_factory=list)


class Synthesis(BaseModel):
    summary: str
    hypotheses: List[str] = Field(default_factory=list)
    experiment_ideas: List[str] = Field(default_factory=list)
    product_implications: List[str] = Field(default_factory=list)
    next_questions: List[str] = Field(default_factory=list)


class MemoryNode(BaseModel):
    id: str
    kind: str
    label: str
    detail: str
    links: List[str] = Field(default_factory=list)
    created_at: datetime


class WorkflowRun(BaseModel):
    id: str
    created_at: datetime
    documents: List[Document]
    analyses: List[DocumentAnalysis]
    comparison: Comparison
    synthesis: Synthesis
    memory_nodes: List[MemoryNode]


class WorkspaceState(BaseModel):
    runs: List[WorkflowRun] = Field(default_factory=list)
    memory_nodes: List[MemoryNode] = Field(default_factory=list)
