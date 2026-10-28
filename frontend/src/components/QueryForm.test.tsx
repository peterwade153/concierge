import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";

import { QueryForm } from "./QueryForm";
import type { RecommendResponse } from "../api/types";
import { makeRecommendation } from "../test/fixtures";

function makeResponse(): RecommendResponse {
  return { recommendation: makeRecommendation() };
}

// Mock the module the component imports so the spy intercepts the real call.
vi.mock("../api/client", () => ({
  getRecommendation: vi.fn(),
}));

import { getRecommendation } from "../api/client";

describe("QueryForm", () => {
  it("renders the textarea, submit button, and example chips", () => {
    render(
      <QueryForm
        isLoading={false}
        setIsLoading={() => {}}
        onResult={() => {}}
        onError={() => {}}
      />
    );

    expect(
      screen.getByPlaceholderText(
        /Find me a good spot for Asian food around the Ntinda or Nakawa neighborhood./
      )
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /get recommendations/i })
    ).toBeInTheDocument();
    expect(screen.getByText("Best Italian food in Kololo")).toBeInTheDocument();
  });

  it("does not submit an empty query", async () => {
    const onResult = vi.fn();
    render(
      <QueryForm
        isLoading={false}
        setIsLoading={() => {}}
        onResult={onResult}
        onError={() => {}}
      />
    );

    await userEvent.click(
      screen.getByRole("button", { name: /get recommendations/i })
    );
    expect(onResult).not.toHaveBeenCalled();
  });

  it("calls onResult with the parsed response on success", async () => {
    const onResult = vi.fn();
    const response = makeResponse();
    (getRecommendation as ReturnType<typeof vi.fn>).mockResolvedValue(response);

    render(
      <QueryForm
        isLoading={false}
        setIsLoading={() => {}}
        onResult={onResult}
        onError={() => {}}
      />
    );

    await userEvent.type(
      screen.getByRole("textbox"),
      "best restaurants in Kololo"
    );
    await userEvent.click(
      screen.getByRole("button", { name: /get recommendations/i })
    );

    expect(getRecommendation).toHaveBeenCalledWith(
      "best restaurants in Kololo",
      expect.any(AbortSignal)
    );
    expect(onResult).toHaveBeenCalledWith(response);
  });

  it("calls onError when the request fails", async () => {
    const onError = vi.fn();
    (getRecommendation as ReturnType<typeof vi.fn>).mockRejectedValue(
      new Error("network down")
    );

    render(
      <QueryForm
        isLoading={false}
        setIsLoading={() => {}}
        onResult={() => {}}
        onError={onError}
      />
    );

    await userEvent.type(screen.getByRole("textbox"), "x");
    await userEvent.click(
      screen.getByRole("button", { name: /get recommendations/i })
    );

    expect(onError).toHaveBeenCalledWith("network down");
  });

  it("disables the button and textarea while loading", () => {
    render(
      <QueryForm
        isLoading
        setIsLoading={() => {}}
        onResult={() => {}}
        onError={() => {}}
      />
    );

    expect(
      screen.getByRole("button", { name: /finding spots/i })
    ).toBeInTheDocument();
    expect(screen.getByRole("textbox")).toBeDisabled();
  });

  it("clicking an example chip populates the textarea", async () => {
    render(
      <QueryForm
        isLoading={false}
        setIsLoading={() => {}}
        onResult={() => {}}
        onError={() => {}}
      />
    );

    await userEvent.click(screen.getByText("Best Italian food in Kololo"));
    expect(screen.getByRole("textbox")).toHaveValue(
      "Best Italian food in Kololo"
    );
  });
});