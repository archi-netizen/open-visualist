import type { ImageResult } from "@/lib/types";
import ImageCard from "./ImageCard";

type Status = "idle" | "waiting" | "analyzing" | "done" | "error";

/**
 * Groups results by the keyword that found them. This is the scoped-down
 * version of design_logic.md's "Sticky Vertical Alignment" — the backend
 * analyzes the whole essay in one pass rather than per-paragraph, so true
 * scroll-synced-to-paragraph suggestions aren't possible yet. Grouping by
 * keyword is the honest version of "anchored to what generated it" that
 * the current API can actually support.
 */
function groupByKeyword(results: ImageResult[]) {
  const groups = new Map<string, ImageResult[]>();
  for (const r of results) {
    const list = groups.get(r.matched_keyword) ?? [];
    list.push(r);
    groups.set(r.matched_keyword, list);
  }
  return Array.from(groups.entries());
}

export default function CurationZone({
  results,
  status,
  errorMessage,
}: {
  results: ImageResult[];
  status: Status;
  errorMessage: string | null;
}) {
  if (status === "error") {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950 dark:text-red-300">
        {errorMessage ?? "Something went wrong reaching the sourcing engine."}
      </div>
    );
  }

  if (status === "idle" || (status === "waiting" && results.length === 0)) {
    return (
      <div className="flex h-full min-h-[40vh] items-center justify-center rounded-lg border border-dashed border-zinc-300 p-6 text-center text-sm text-zinc-400 dark:border-zinc-700">
        Sourced public-domain images will appear here, grouped by the visual
        hook they matched.
      </div>
    );
  }

  const groups = groupByKeyword(results);

  return (
    <div className="space-y-6">
      {status === "analyzing" && (
        <p className="text-xs text-zinc-500 dark:text-zinc-400">Sourcing images…</p>
      )}

      {groups.length === 0 && status === "done" && (
        <div className="rounded-lg border border-dashed border-zinc-300 p-6 text-center text-sm text-zinc-400 dark:border-zinc-700">
          No public-domain matches found for this draft yet — try adding more
          concrete, visual detail.
        </div>
      )}

      {groups.map(([keyword, images]) => (
        <div key={keyword}>
          <span className="mb-2 inline-block rounded-full bg-teal-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-teal-800 dark:bg-teal-950 dark:text-teal-300">
            {keyword}
          </span>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {images.map((img) => (
              <ImageCard key={img.url} result={img} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
