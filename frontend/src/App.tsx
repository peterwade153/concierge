import { useState } from "react";

import { ErrorBanner } from "./components/ErrorBanner";
import { QueryForm } from "./components/QueryForm";
import { RecommendationView } from "./components/RecommendationView";
import type { RecommendResponse } from "./api/types";

export function App() {
  const [result, setResult] = useState<RecommendResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  function clearError() {
    setError(null);
  }

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 py-10 sm:py-16">
      <header className="space-y-2 text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-brand-500 text-white">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            className="h-7 w-7"
            aria-hidden="true"
          >
            <path d="M11.5 2c.3 0 .5.2.5.5V4h2v-.5c0-.3.2-.5.5-.5s.5.2.5.5V4h1.3A3.2 3.2 0 0 1 20 7.2v1.3h-.5c-.3 0-.5.2-.5.5s.2.5.5.5h.5v1.3a3.2 3.2 0 0 1-3.2 3.2h-1.3v.5c0 .3-.2.5-.5.5s-.5-.2-.5-.5v-.5H9.7A3.2 3.2 0 0 1 6.5 13V12h.5c.3 0 .5-.2.5-.5s-.2-.5-.5-.5h-.5V9.7A3.2 3.2 0 0 1 8.2 6.5h1.3V6h-.5c-.3 0-.5-.2-.5-.5s.2-.5.5-.5h.5V4H8.2A3.2 3.2 0 0 1 5 7.2v1.3H3.5c-.3 0-.5.2-.5.5s.2.5.5.5H3v1.3a3.2 3.2 0 0 0 3.2 3.2h1.3v.5c0 .3.2.5.5.5s.5-.2.5-.5v-.5h4.6v.5c0 .3.2.5.5.5s.5-.2.5-.5v-.5h1.3A3.2 3.2 0 0 0 20 12V10.7h.5c.3 0 .5-.2.5-.5s-.2-.5-.5-.5h-.5V8.2A3.2 3.2 0 0 0 16.3 5H15V3.5c0-.3-.2-.5-.5-.5s-.5.2-.5.5V5h-2V3.5c0-.3-.2-.5-.5-.5ZM8.2 8.2h-.5V9.7h.5V8.2Zm0 3.2h-.5V12h.5V11.4Zm1.3 1.3h4.6v1.3h-4.6v-1.3Zm6.5-1.3h.5V9.7h-.5V8.2Z" />
          </svg>
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-brand-900 sm:text-4xl">
          Concierge
        </h1>
        <p className="text-base text-slate-500">
          Fine dining recommendations by neighborhood.
        </p>
      </header>

      <QueryForm
        isLoading={isLoading}
        setIsLoading={setIsLoading}
        onResult={(data) => {
          setError(null);
          setResult(data);
        }}
        onError={(msg) => {
          setError(msg);
          setResult(null);
        }}
      />

      {error && <ErrorBanner message={error} onDismiss={clearError} />}

      {result && <RecommendationView data={result.recommendation} />}

      {!result && !error && !isLoading && (
        <p className="text-center text-sm text-slate-400">
          Ask for a spot and we will find the best restaurants nearby.
        </p>
      )}
    </div>
  );
}