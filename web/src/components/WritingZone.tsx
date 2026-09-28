"use client";

type Status = "idle" | "waiting" | "analyzing" | "done" | "error";

const STATUS_LABEL: Record<Status, string> = {
  idle: "Start writing — suggestions appear after a pause",
  waiting: "Waiting for a pause in typing…",
  analyzing: "Reading your draft…",
  done: "Up to date",
  error: "Couldn't reach the sourcing engine",
};

export default function WritingZone({
  value,
  onChange,
  status,
}: {
  value: string;
  onChange: (v: string) => void;
  status: Status;
}) {
  return (
    <div className="flex h-full flex-col">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste or write your essay here. OpenVisualist reads it 3 seconds after you stop typing and suggests public-domain images for what it finds."
        className="h-full min-h-[60vh] w-full flex-1 resize-none rounded-lg border border-zinc-200 bg-white p-4 font-serif text-lg leading-relaxed text-zinc-900 outline-none focus:border-teal-500 dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-100"
      />
      <p
        className={`mt-2 text-xs ${
          status === "error" ? "text-red-600" : "text-zinc-500 dark:text-zinc-400"
        }`}
      >
        {STATUS_LABEL[status]}
      </p>
    </div>
  );
}
