
from pydantic import BaseModel, Field


class RestaurantDetails(BaseModel):
    name: str = Field(description="The full name of the restaurant.")
    location: str = Field(description="The physical street address and neighborhood area.")
    cuisine: list[str] = Field(description="List of food types served.", default=[])
    price_range: str | None = Field(description="The rough cost per person in local currency (e.g., UGX).", default=None)
    rating: float | None = Field(description="The numerical rating out of 5 stars.", default=None)
    specialty: str | None = Field(description="A short description of their signature dish and atmosphere.", default=None)

class RestaurantRecommendations(BaseModel):
    neighborhood_searched: str = Field(description="The area requested by the user.")
    recommended_spots: list[RestaurantDetails] = Field(description="A list of matching restaurant options.")
    summary_verdict: str = Field(description="A friendly concluding wrap-up sentence from the concierge.")
