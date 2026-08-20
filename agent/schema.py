from pydantic import BaseModel, Field
from typing import List

class RestaurantDetails(BaseModel):
    name: str = Field(description="The full name of the restaurant.")
    location: str = Field(description="The physical street address and neighborhood area.")
    cuisine: List[str] = Field(description="List of food types served.")
    price_range: str = Field(description="The rough cost per person in local currency (e.g., UGX).")
    rating: float = Field(description="The numerical rating out of 5 stars.")
    specialty: str = Field(description="A short description of their signature dish and atmosphere.")

class RestaurantRecommendations(BaseModel):
    neighborhood_searched: str = Field(description="The area requested by the user.")
    recommended_spots: List[RestaurantDetails] = Field(description="A list of matching restaurant options.")
    summary_verdict: str = Field(description="A friendly concluding wrap-up sentence from the concierge.")