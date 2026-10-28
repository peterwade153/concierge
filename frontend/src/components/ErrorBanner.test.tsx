import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";

import { ErrorBanner } from "./ErrorBanner";

describe("ErrorBanner", () => {
  it("renders the error message", () => {
    render(<ErrorBanner message="boom" onDismiss={() => {}} />);
    expect(screen.getByText("boom")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toBeInTheDocument();
  });

  it("calls onDismiss when the dismiss button is clicked", async () => {
    const onDismiss = vi.fn();
    render(<ErrorBanner message="x" onDismiss={onDismiss} />);

    await userEvent.click(screen.getByRole("button", { name: /dismiss error/i }));
    expect(onDismiss).toHaveBeenCalledTimes(1);
  });
});