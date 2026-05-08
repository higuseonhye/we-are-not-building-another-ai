# We Are Not Building Another AI

Most AI tools generate answers.

We are building systems that help humans:

- think deeper
- synthesize better
- track reasoning
- compare perspectives
- evolve ideas over time

This is cognitive workflow infrastructure for the AI era.

![Product demo screenshot](docs/product-demo.png)

## What This Is

This repository is a product, manifesto, research lab, and prototype for a new category of AI-native knowledge work.

It is not another chatbot, AI assistant, chat-with-PDF wrapper, or generic automation layer.

It is a thinking workspace for people who work with complex ideas: founders, COOs, PM leaders, strategy teams, researchers, and cross-functional operators.

The core belief is simple: modern organizations are not suffering from lack of information. They are suffering from fragmented context, shallow synthesis, lost reasoning, decision fatigue, organizational memory loss, invisible tradeoffs, and coordination complexity.

These people do not need more AI answers.

They need better cognitive leverage.

## First MVP

Build one deep workflow:

```text
Research -> Critique -> Comparison -> Synthesis -> Hypothesis
```

The MVP helps users upload documents, research papers, transcripts, meeting notes, and memos. It extracts key claims, assumptions, contradictions, weak points, uncertainty, and missing perspectives. It compares competing ideas, strategic tradeoffs, conflicting assumptions, and consensus versus disagreement. It generates synthesis, hypotheses, strategic implications, experiment ideas, and unresolved questions. It stores evolving reasoning in a lightweight memory layer.

## Product Philosophy

The system should help users answer:

- Why did we make this decision?
- What assumptions did we make?
- What alternatives existed?
- What uncertainty remained?
- What tradeoffs were considered?
- How has our thinking evolved?

The product should feel reflective, calm, strategic, deep, and reasoning-oriented.

It should not feel flashy, noisy, gimmicky, or like a generic AI productivity tool.

## Repository Structure

```text
apps/
  web/      Next.js + Tailwind synthesis workspace
  api/      FastAPI backend

core/
  workflow/    research-loop orchestration, schemas, ingestion
  critique/    claims, assumptions, weak points, uncertainty
  comparison/  consensus, disagreement, conflicting logic
  synthesis/   synthesis, hypotheses, implications, next questions
  memory/      persistent memory and linked reasoning nodes
  reasoning/   shared reasoning utilities

agents/
  critic/
  synthesizer/
  hypothesis/
  evaluator/

research/
  cognitive-workflows/
  decision-systems/
  thought-augmentation/
  organizational-cognition/

docs/
  manifesto.md
  vision.md
  product-principles.md
  architecture.md
  cognitive-friction.md

examples/
  research-loop/
  strategy-loop/
  decision-loop/
```

## Technical Stack

- Next.js
- Tailwind
- TypeScript
- Python backend
- FastAPI
- lightweight JSON memory layer
- modular core and agent architecture
- future OpenAI / Claude adapters behind agent interfaces

Keep the system clean, extensible, composable, and fast to iterate.

## Run Locally

Backend:

```bash
cd apps/api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

Frontend:

```bash
cd apps/web
npm install
npm run dev -- -p 3001
```

Open `http://localhost:3001`.

Upload the example memos in `examples/research-loop`.

## Build Priorities

1. Cognitive workflow quality
2. Synthesis quality
3. Strategic reasoning
4. Memory continuity
5. Comparison and critique
6. Simplicity
7. Daily usability

Lower priority:

- scaling infra
- enterprise auth
- flashy UI
- complex agent orchestration

## Brand Narrative

This product exists because AI should not only automate work.

It should help humans think better, decide better, collaborate better, reclaim cognitive clarity, and reclaim time for meaningful life.

We believe:

- time is the new luxury
- creativity is the new power
- meaningful work matters
- cognition is becoming infrastructure

The goal is for this repository to feel like the beginning of a new category.

Not another AI tool.
