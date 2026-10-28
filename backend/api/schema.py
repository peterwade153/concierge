from pydantic import BaseModel
from agent.schema import RestaurantRecommendations


class RecommendRequest(BaseModel):
    query: str


class RecommendResponse(BaseModel):
    recommendation: RestaurantRecommendations
