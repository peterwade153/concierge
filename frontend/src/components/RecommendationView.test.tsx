import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

import { RecommendationView } from "./RecommendationView";
import { makeRecommendation } from "../test/fixtures";

describe("RecommendationView", () => {
  it("renders the neighborhood and summary verdict", () => {
    render(<RecommendationView data={makeRecommendation()} />);

    expect(screen.getByText("Kampala")).toBeInTheDocument();
    expect(
      screen.getByText(
        "You will love The Lamu House for its authentic Swahili flavors."
      )
    ).toBeInTheDocument();
  });

  it("renders each recommended spot", () => {
    render(<RecommendationView data={makeRecommendation()} />);
    expect(screen.getByText("The Lamu House")).toBeInTheDocument();
  });

  it("renders an empty state when there are no spots", () => {
    render(
      <RecommendationView
        data={makeRecommendation({ recommended_spots: [] })}
      />
    );
    expect(
      screen.getByText("No recommendations were found for this area.")
    ).toBeInTheDocument();
  });
});