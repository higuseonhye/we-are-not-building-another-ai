"use client";

import { ChangeEvent, useEffect, useMemo, useState } from "react";
import {
  Brain,
  GitCompareArrows,
  Lightbulb,
  LucideIcon,
  Loader2,
  MemoryStick,
  Microscope,
  Upload,
} from "lucide-react";

type DocumentAnalysis = {
  document_id: string;
  title: string;
  key_claims: string[];
  assumptions: string[];
  weak_points: string[];
  uncertainties: string[];
  contradictions: string[];
  alternative_framings: string[];
};

type WorkflowRun = {
  id: string;
  created_at: string;
  documents: { id: string; title: string; source_type: string }[];
  analyses: DocumentAnalysis[];
  comparison: {
    consensus: string[];
    disagreements: string[];
    hidden_assumptions: string[];
    conflicting_logic: string[];
  };
  synthesis: {
    summary: string;
    hypotheses: string[];
    experiment_ideas: string[];
    product_implications: string[];
    next_questions: string[];
  };
  memory_nodes: { id: string; kind: string; label: string; detail: string }[];
};

type WorkspaceState = {
  runs: WorkflowRun[];
  memory_nodes: { id: string; kind: string; label: string; detail: string }[];
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8010";

const stages = [
  { label: "Research", icon: Microscope },
  { label: "Critique", icon: Brain },
  { label: "Comparison", icon: GitCompareArrows },
  { label: "Synthesis", icon: Lightbulb },
  { label: "Memory", icon: MemoryStick },
];

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [activeRun, setActiveRun] = useState<WorkflowRun | null>(null);
  const [workspace, setWorkspace] = useState<WorkspaceState | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/workspace`)
      .then((response) => response.json())
      .then((state: WorkspaceState) => {
        setWorkspace(state);
        setActiveRun(state.runs[0] ?? null);
      })
      .catch(() => setWorkspace({ runs: [], memory_nodes: [] }));
  }, []);

  const selectedNames = useMemo(() => files.map((file) => file.name).join(", "), [files]);

  function onFiles(event: ChangeEvent<HTMLInputElement>) {
    setError("");
    setFiles(Array.from(event.target.files ?? []));
  }

  async function runWorkflow() {
    if (!files.length) {
      setError("Add at least one document.");
      return;
    }

    setLoading(true);
    setError("");
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const response = await fetch(`${API_BASE}/workflows/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const payload = await response.json();
        throw new Error(payload.detail ?? "Analysis failed.");
      }

      const run: WorkflowRun = await response.json();
      setActiveRun(run);
      setWorkspace((current) => ({
        runs: [run, ...(current?.runs ?? [])],
        memory_nodes: [...run.memory_nodes, ...(current?.memory_nodes ?? [])],
      }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-paper">
      <section className="border-b border-ink/10 bg-[#faf8f0]">
        <div className="mx-auto flex max-w-7xl flex-col gap-8 px-5 py-7 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-rust">Cognitive Workflow Infrastructure</p>
            <h1 className="mt-3 text-4xl font-semibold leading-tight text-ink md:text-6xl">A workspace for evolving thought.</h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-ink/70">
              Upload source material, expose its reasoning, compare tensions, and turn uncertainty into hypotheses worth carrying forward.
            </p>
          </div>
          <div className="grid grid-cols-5 gap-2 lg:w-[520px]">
            {stages.map(({ label, icon: Icon }) => (
              <div key={label} className="flex min-h-24 flex-col items-center justify-center gap-2 border border-ink/10 bg-white/70 p-3 text-center">
                <Icon className="h-5 w-5 text-tide" aria-hidden="true" />
                <span className="text-xs font-medium text-ink/75">{label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl grid-cols-1 gap-5 px-5 py-6 lg:grid-cols-[340px_minmax(0,1fr)]">
        <aside className="space-y-5">
          <div className="border border-ink/10 bg-white p-4 shadow-soft">
            <label className="flex min-h-40 cursor-pointer flex-col items-center justify-center gap-3 border border-dashed border-ink/25 bg-[#fbfaf5] p-5 text-center">
              <Upload className="h-7 w-7 text-moss" aria-hidden="true" />
              <span className="text-sm font-semibold">Upload research material</span>
              <span className="text-xs leading-5 text-ink/60">TXT, Markdown, or PDF</span>
              <input className="sr-only" type="file" multiple accept=".txt,.md,.pdf" onChange={onFiles} />
            </label>
            {selectedNames ? <p className="mt-3 text-sm leading-5 text-ink/70">{selectedNames}</p> : null}
            {error ? <p className="mt-3 text-sm text-rust">{error}</p> : null}
            <button
              onClick={runWorkflow}
              disabled={loading}
              className="mt-4 flex w-full items-center justify-center gap-2 bg-ink px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Brain className="h-4 w-4" aria-hidden="true" />}
              Run cognitive loop
            </button>
          </div>

          <MemoryPanel workspace={workspace} onSelect={setActiveRun} />
        </aside>

        <section className="min-w-0">
          {activeRun ? <RunView run={activeRun} /> : <EmptyState />}
        </section>
      </section>
    </main>
  );
}

function EmptyState() {
  return (
    <div className="flex min-h-[560px] items-center justify-center border border-ink/10 bg-white p-8 text-center shadow-soft">
      <div className="max-w-md">
        <Brain className="mx-auto h-10 w-10 text-tide" aria-hidden="true" />
        <h2 className="mt-4 text-2xl font-semibold">Begin with source material.</h2>
        <p className="mt-3 leading-7 text-ink/60">
          The first useful surface is not a blank chat box. It is a structured read of what your documents claim, assume, miss, and make possible.
        </p>
      </div>
    </div>
  );
}

function MemoryPanel({
  workspace,
  onSelect,
}: {
  workspace: WorkspaceState | null;
  onSelect: (run: WorkflowRun) => void;
}) {
  return (
    <div className="border border-ink/10 bg-white p-4 shadow-soft">
      <div className="flex items-center gap-2">
        <MemoryStick className="h-4 w-4 text-moss" aria-hidden="true" />
        <h2 className="text-sm font-semibold uppercase tracking-[0.14em] text-ink/70">Memory</h2>
      </div>
      <div className="mt-4 space-y-3">
        {(workspace?.runs ?? []).slice(0, 4).map((run) => (
          <button key={run.id} onClick={() => onSelect(run)} className="w-full border border-ink/10 p-3 text-left hover:bg-[#fbfaf5]">
            <p className="text-sm font-medium">{run.documents.map((document) => document.title).join(" + ")}</p>
            <p className="mt-1 text-xs text-ink/50">{new Date(run.created_at).toLocaleString()}</p>
          </button>
        ))}
        {!workspace?.runs?.length ? <p className="text-sm leading-6 text-ink/60">Durable hypotheses and questions will collect here.</p> : null}
      </div>
    </div>
  );
}

function RunView({ run }: { run: WorkflowRun }) {
  return (
    <div className="space-y-5">
      <div className="border border-ink/10 bg-white p-5 shadow-soft">
        <p className="text-sm font-semibold uppercase tracking-[0.14em] text-rust">Synthesis</p>
        <h2 className="mt-3 text-3xl font-semibold">Working model</h2>
        <p className="mt-4 max-w-4xl text-lg leading-8 text-ink/75">{run.synthesis.summary}</p>
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <Panel title="Hypotheses" icon={Lightbulb} items={run.synthesis.hypotheses} tone="tide" />
        <Panel title="Next Questions" icon={Brain} items={run.synthesis.next_questions} tone="rust" />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <Panel title="Consensus" icon={GitCompareArrows} items={run.comparison.consensus} tone="moss" />
        <Panel title="Disagreements" icon={GitCompareArrows} items={run.comparison.disagreements} tone="rust" />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        {run.analyses.map((analysis) => (
          <DocumentCard key={analysis.document_id} analysis={analysis} />
        ))}
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <Panel title="Experiments" icon={Microscope} items={run.synthesis.experiment_ideas} tone="tide" />
        <Panel title="Product Implications" icon={MemoryStick} items={run.synthesis.product_implications} tone="moss" />
      </div>
    </div>
  );
}

function DocumentCard({ analysis }: { analysis: DocumentAnalysis }) {
  return (
    <article className="border border-ink/10 bg-white p-5 shadow-soft">
      <p className="text-sm font-semibold uppercase tracking-[0.14em] text-tide">Critique</p>
      <h3 className="mt-2 text-2xl font-semibold">{analysis.title}</h3>
      <div className="mt-5 grid gap-4">
        <MiniSection title="Key claims" items={analysis.key_claims} />
        <MiniSection title="Assumptions" items={analysis.assumptions} />
        <MiniSection title="Weak points" items={analysis.weak_points} />
        <MiniSection title="Uncertainty" items={analysis.uncertainties} />
        <MiniSection title="Alternative framings" items={analysis.alternative_framings} />
      </div>
    </article>
  );
}

function Panel({
  title,
  icon: Icon,
  items,
  tone,
}: {
  title: string;
  icon: LucideIcon;
  items: string[];
  tone: "moss" | "rust" | "tide";
}) {
  const toneClass = tone === "moss" ? "text-moss" : tone === "rust" ? "text-rust" : "text-tide";
  return (
    <section className="border border-ink/10 bg-white p-5 shadow-soft">
      <div className="flex items-center gap-2">
        <Icon className={`h-4 w-4 ${toneClass}`} aria-hidden="true" />
        <h3 className="text-sm font-semibold uppercase tracking-[0.14em] text-ink/70">{title}</h3>
      </div>
      <ul className="mt-4 space-y-3">
        {items.map((item, index) => (
          <li key={`${title}-${index}`} className="border-l-2 border-flax pl-3 text-sm leading-6 text-ink/75">
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}

function MiniSection({ title, items }: { title: string; items: string[] }) {
  return (
    <section>
      <h4 className="text-sm font-semibold text-ink">{title}</h4>
      <ul className="mt-2 space-y-2">
        {items.length ? (
          items.map((item, index) => (
            <li key={`${title}-${index}`} className="text-sm leading-6 text-ink/70">
              {item}
            </li>
          ))
        ) : (
          <li className="text-sm leading-6 text-ink/50">No explicit signal detected.</li>
        )}
      </ul>
    </section>
  );
}
