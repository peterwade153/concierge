interface ErrorBannerProps {
  message: string;
  onDismiss: () => void;
}

export function ErrorBanner({ message, onDismiss }: ErrorBannerProps) {
  return (
    <div
      role="alert"
      className="flex items-start justify-between gap-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 shadow-sm"
    >
      <span className="font-medium">Something went wrong.</span>
      <span className="text-red-500">{message}</span>
      <button
        type="button"
        onClick={onDismiss}
        aria-label="Dismiss error"
        className="shrink-0 rounded px-2 py-1 text-red-400 hover:bg-red-100 hover:text-red-600"
      >
        Dismiss
      </button>
    </div>
  );
}