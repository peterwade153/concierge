import { useEffect, useRef, useState } from "react";

import { getRecommendation } from "../api/client";
import type { RecommendResponse } from "../api/types";

const EXAMPLE_QUERIES = [
  "Best Italian food in Kololo",
  "Fine dining with seafood in Nakawa",
  "Romantic Asian restaurants in Ntinda",
];

interface QueryFormProps {
  isLoading: boolean;
  setIsLoading: (value: boolean) => void;
  onResult: (data: RecommendResponse) => void;
  onError: (message: string) => void;
}

export function QueryForm({
  isLoading,
  setIsLoading,
  onResult,
  onError,
}: QueryFormProps) {
  const [query, setQuery] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  // Cancel any in-flight request when the component unmounts.
  useEffect(() => {
    return () => {
      if (abortRef.current) {
        abortRef.current.abort();
      }
    };
  }, []);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const trimmed = query.trim();
    if (!trimmed || isLoading) return;

    const controller = new AbortController();
    abortRef.current = controller;

    setIsLoading(true);
    try {
      const data = await getRecommendation(trimmed, controller.signal);
      onResult(data);
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        return;
      }
      onError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <label htmlFor="query" className="sr-only">
        Restaurant query
      </label>
      <textarea
        id="query"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        rows={3}
        disabled={isLoading}
        placeholder="e.g. Find me a good spot for Asian food around the Ntinda or Nakawa neighborhood."
        className="w-full resize-y rounded-lg border border-slate-300 bg-white px-4 py-3 text-sm text-slate-800 shadow-sm outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-200 disabled:bg-slate-100"
      />

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <button
          type="submit"
          disabled={isLoading}
          className="inline-flex items-center justify-center rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-600 focus:outline-none focus:ring-2 focus:ring-brand-300 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-brand-300"
        >
          {isLoading ? (
            <>
              <svg
                className="mr-2 h-4 w-4 animate-spin"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-90"
                  fill="currentColor"
                  d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              Finding spots...
            </>
          ) : (
            "Get Recommendations"
          )}
        </button>

        <div className="flex flex-wrap gap-2">
          {EXAMPLE_QUERIES.map((example) => (
            <button
              key={example}
              type="button"
              disabled={isLoading}
              onClick={() => setQuery(example)}
              className="rounded-full border border-slate-300 bg-white px-3 py-1 text-xs font-medium text-slate-600 transition hover:border-brand-400 hover:text-brand-700 disabled:opacity-50"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </form>
  );
}