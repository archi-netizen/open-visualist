import type { ImageResult } from "@/lib/types";

/**
 * Green Shield: Public Domain (CC0/PDM) — no attribution required.
 * Yellow Shield: attribution required (CC-BY and its variants).
 * This collapses several distinct licenses into two shields per
 * design_logic.md — some "yellow" licenses (NC/ND variants) also restrict
 * commercial use or derivatives, which a single shield can't convey, so the
 * license code and link are always shown alongside it.
 */
export default function LicenseShield({ result }: { result: ImageResult }) {
  const isGreen = !result.requires_attribution;
  return (
    <a
      href={result.license_url}
      target="_blank"
      rel="noopener noreferrer"
      title={
        isGreen
          ? "Public domain — no attribution required"
          : "Attribution required — see license for any other conditions"
      }
      className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ${
        isGreen
          ? "bg-emerald-100 text-emerald-800"
          : "bg-amber-100 text-amber-800"
      }`}
    >
      <span aria-hidden>{isGreen ? "🛡️" : "🛡️"}</span>
      {result.license_code.toUpperCase()}
    </a>
  );
}
