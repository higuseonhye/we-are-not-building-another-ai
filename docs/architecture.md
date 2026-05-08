# Architecture

The repository is organized as a product plus research lab.

```text
apps/
  web/      Next.js thinking workspace
  api/      FastAPI interface

core/
  workflow/    orchestration, schemas, ingestion
  critique/    claim, assumption, weak-point extraction
  comparison/  consensus, disagreement, tradeoff analysis
  synthesis/   synthesis and working-model generation
  memory/      persistence and memory-node construction
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

examples/
  research-loop/
  strategy-loop/
  decision-loop/
```

The current implementation uses deterministic local heuristics so the workflow is usable without API keys. OpenAI or Claude adapters should be added behind the agent interfaces, not directly inside UI components.

The API should stay thin. Product intelligence belongs in `core` and `agents`.
