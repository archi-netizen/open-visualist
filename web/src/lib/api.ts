import type { ImageResult } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class AnalyzeError extends Error {}

/** Calls the backend's /analyze-and-source endpoint with the current essay text. */
export async function analyzeAndSource(
  content: string,
  signal?: AbortSignal,
): Promise<ImageResult[]> {
  const response = await fetch(`${API_URL}/analyze-and-source`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
    signal,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch {
      // response wasn't JSON — fall back to statusText
    }
    throw new AnalyzeError(detail);
  }

  return response.json();
}
