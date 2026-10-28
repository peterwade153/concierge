import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

import { App } from "./App";

describe("App", () => {
  it("renders the header and empty state on first render", () => {
    render(<App />);

    expect(screen.getByText("Concierge")).toBeInTheDocument();
    expect(
      screen.getByText("Fine dining recommendations by neighborhood.")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Ask for a spot and we will find the best restaurants nearby.")
    ).toBeInTheDocument();
  });
});