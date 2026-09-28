"use client";

import { useState } from "react";
import type { ImageResult } from "@/lib/types";
import LicenseShield from "./LicenseShield";

export default function ImageCard({ result }: { result: ImageResult }) {
  const [copied, setCopied] = useState(false);

  async function copyAttribution() {
    try {
      await navigator.clipboard.writeText(result.attribution);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard API can be unavailable (e.g. insecure context) — no-op.
    }
  }

  return (
    <div className="overflow-hidden rounded-lg border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
      <a href={result.foreign_landing_url} target="_blank" rel="noopener noreferrer">
        {/* eslint-disable-next-line @next/next/no-img-element -- arbitrary external hosts, next/image would need a wildcard remotePatterns config */}
        <img
          src={result.thumbnail}
          alt={result.title}
          className="h-40 w-full object-cover"
          loading="lazy"
        />
      </a>
      <div className="space-y-2 p-3">
        <div className="flex items-start justify-between gap-2">
          <p className="line-clamp-2 text-sm font-medium text-zinc-900 dark:text-zinc-100">
            {result.title}
          </p>
          <LicenseShield result={result} />
        </div>

        <p className="text-xs text-zinc-500 dark:text-zinc-400">
          by {result.creator} · {result.source}
        </p>

        {/* Confidence meter — see the heuristic note in api/sourcing.py; this
            is a keyword/title overlap score, not an AI verification pass. */}
        <div>
          <div className="mb-1 flex justify-between text-[11px] text-zinc-500 dark:text-zinc-400">
            <span>Match strength</span>
            <span>{result.confidence}%</span>
          </div>
          <div className="h-1.5 w-full rounded-full bg-zinc-200 dark:bg-zinc-800">
            <div
              className="h-1.5 rounded-full bg-teal-500"
              style={{ width: `${result.confidence}%` }}
            />
          </div>
        </div>

        <button
          type="button"
          onClick={copyAttribution}
          className="w-full rounded-md border border-zinc-300 px-2 py-1 text-xs font-medium text-zinc-700 transition-colors hover:bg-zinc-50 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
        >
          {copied ? "Copied ✓" : "Copy attribution"}
        </button>
      </div>
    </div>
  );
}
