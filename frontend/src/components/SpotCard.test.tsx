import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

import { SpotCard } from "./SpotCard";
import type { RestaurantDetails } from "../api/types";

const spot: RestaurantDetails = {
  name: "The Lamu House",
  location: "Kampala Road",
  cuisine: ["Swahili", "Seafood"],
  price_range: "UGX 25,000",
  rating: 4.5,
  specialty: "Freshly caught fish with coastal spices.",
};

describe("SpotCard", () => {
  it("renders name, location, and cuisine", () => {
    render(<SpotCard spot={spot} />);

    expect(screen.getByText("The Lamu House")).toBeInTheDocument();
    expect(screen.getByText("Kampala Road")).toBeInTheDocument();
    expect(screen.getByText("Swahili")).toBeInTheDocument();
    expect(screen.getByText("Seafood")).toBeInTheDocument();
  });

  it("renders the rating badge when a rating is present", () => {
    render(<SpotCard spot={spot} />);
    expect(screen.getByText(/4\.5/)).toBeInTheDocument();
  });

  it("renders the price range and specialty", () => {
    render(<SpotCard spot={spot} />);
    expect(screen.getByText("UGX 25,000")).toBeInTheDocument();
    expect(
      screen.getByText("Freshly caught fish with coastal spices.")
    ).toBeInTheDocument();
  });

  it("does not render a rating badge when rating is null", () => {
    render(<SpotCard spot={{ ...spot, rating: null }} />);
    expect(screen.queryByText(/★/)).not.toBeInTheDocument();
  });

  it("does not render cuisine tags when the list is empty", () => {
    render(<SpotCard spot={{ ...spot, cuisine: [] }} />);
    expect(screen.queryByText("Swahili")).not.toBeInTheDocument();
  });
});