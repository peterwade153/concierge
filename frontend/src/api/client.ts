import type { RecommendRequest, RecommendResponse } from "./types";

const ENDPOINT = "/api/recommend";

async function readErrorDetail(res: Response): Promise<string | null> {
  try {
    const data = await res.json();
    if (data && typeof data.detail === "string") {
      return data.detail;
    }
    return null;
  } catch {
    return null;
  }
}

export async function getRecommendation(
  query: string,
  signal?: AbortSignal
): Promise<RecommendResponse> {
  const body: RecommendRequest = { query };

  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });

  if (!res.ok) {
    const detail = await readErrorDetail(res);
    throw new Error(detail ?? `Request failed with status ${res.status}`);
  }

  return (await res.json()) as RecommendResponse;
}