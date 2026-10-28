export interface RestaurantDetails {
  name: string;
  location: string;
  cuisine: string[];
  price_range: string | null;
  rating: number | null;
  specialty: string | null;
}

export interface RestaurantRecommendations {
  neighborhood_searched: string;
  recommended_spots: RestaurantDetails[];
  summary_verdict: string;
}

export interface RecommendRequest {
  query: string;
}

export interface RecommendResponse {
  recommendation: RestaurantRecommendations;
}