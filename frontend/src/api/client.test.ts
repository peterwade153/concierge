import { describe, it, expect, vi } from "vitest";

import { getRecommendation } from "./client";
import type { RecommendResponse } from "./types";
import { makeRecommendation } from "../test/fixtures";

function mockResponse(status: number, body: unknown): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as unknown as Response;
}

describe("getRecommendation", () => {
  it("POSTs the query to /api/recommend", async () => {
    const fetchSpy = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(mockResponse(200, {
        recommendation: makeRecommendation(),
      }));

    await getRecommendation("best in Kololo");

    expect(fetchSpy).toHaveBeenCalledWith(
      "/api/recommend",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: "best in Kololo" }),
      })
    );
  });

  it("returns the parsed response on success", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      mockResponse(200, { recommendation: makeRecommendation() })
    );

    const result: RecommendResponse = await getRecommendation("x");
    expect(result.recommendation.neighborhood_searched).toBe("Kampala");
  });

  it("throws with the API detail message on a 502", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      mockResponse(502, { detail: "Agent returned no recommendation." })
    );

    await expect(getRecommendation("x")).rejects.toThrow(
      "Agent returned no recommendation."
    );
  });

  it("throws a status-based message when there is no detail body", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(500, {}));

    await expect(getRecommendation("x")).rejects.toThrow(
      "Request failed with status 500"
    );
  });

  it("forwards the AbortSignal to fetch", async () => {
    const fetchSpy = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(mockResponse(200, { recommendation: makeRecommendation() }));

    const controller = new AbortController();
    await getRecommendation("x", controller.signal);

    expect(fetchSpy).toHaveBeenCalledWith(
      "/api/recommend",
      expect.objectContaining({ signal: controller.signal })
    );
  });
});