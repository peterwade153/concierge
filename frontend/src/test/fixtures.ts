import type { RestaurantRecommendations } from "../api/types";

export function makeRecommendation(
  overrides: Partial<RestaurantRecommendations> = {}
): RestaurantRecommendations {
  return {
    neighborhood_searched: "Kampala",
    recommended_spots: [
      {
        name: "The Lamu House",
        location: "Kampala Road",
        cuisine: ["Swahili", "Seafood"],
        price_range: "UGX 25,000",
        rating: 4.5,
        specialty: "Freshly caught fish with coastal spices.",
      },
    ],
    summary_verdict: "You will love The Lamu House for its authentic Swahili flavors.",
    ...overrides,
  };
}