"use client";

import { useEffect, useRef, useState } from "react";
import WritingZone from "@/components/WritingZone";
import CurationZone from "@/components/CurationZone";
import { analyzeAndSource, AnalyzeError } from "@/lib/api";
import type { ImageResult } from "@/lib/types";

type Status = "idle" | "waiting" | "analyzing" | "done" | "error";

// "Debounce Processing... waits for a 3000ms pause" — design_logic.md §1
const DEBOUNCE_MS = 3000;

export default function Home() {
  const [content, setContent] = useState("");
  const [results, setResults] = useState<ImageResult[]>([]);
  const [status, setStatus] = useState<Status>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  function handleChange(next: string) {
    setContent(next);

    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (abortRef.current) abortRef.current.abort();

    if (!next.trim()) {
      setStatus("idle");
      setResults([]);
      return;
    }

    setStatus("waiting");
    debounceRef.current = setTimeout(() => runAnalysis(next), DEBOUNCE_MS);
  }

  async function runAnalysis(text: string) {
    const controller = new AbortController();
    abortRef.current = controller;
    setStatus("analyzing");
    setErrorMessage(null);

    try {
      const found = await analyzeAndSource(text, controller.signal);
      setResults(found);
      setStatus("done");
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") return;
      setErrorMessage(err instanceof AnalyzeError ? err.message : "Network error.");
      setStatus("error");
    }
  }

  useEffect(() => {
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
      if (abortRef.current) abortRef.current.abort();
    };
  }, []);

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-6 p-6">
      <header>
        <h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-100">
          OpenVisualist
        </h1>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          Context-aware image sourcing for the Public Domain.
        </p>
      </header>

      <main className="grid flex-1 grid-cols-1 gap-6 lg:grid-cols-[3fr_2fr]">
        <section aria-label="Writing zone">
          <WritingZone value={content} onChange={handleChange} status={status} />
        </section>
        <section aria-label="Curation zone" className="lg:overflow-y-auto">
          <CurationZone results={results} status={status} errorMessage={errorMessage} />
        </section>
      </main>
    </div>
  );
}
