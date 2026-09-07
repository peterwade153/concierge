import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app
from agent.schema import RestaurantRecommendations, RestaurantDetails


client = TestClient(app)


@pytest.fixture
def mock_restaurant_agent():
    with patch("api.main.RestaurantAgent") as MockAgent:
        yield MockAgent


def make_mock_recommendation():
    return RestaurantRecommendations(
        neighborhood_searched="Kampala",
        recommended_spots=[
            RestaurantDetails(
                name="The Lamu House",
                location="Kampala Road",
                cuisine=["Swahili", "Seafood"],
                price_range="UGX 25,000",
                rating=4.5,
                specialty="Freshly caught fish with coastal spices.",
            )
        ],
        summary_verdict="You will love The Lamu House for its authentic Swahili flavors.",
    )


class TestRecommendEndpoint:
    def test_recommend_success(self, mock_restaurant_agent):
        mock_result = make_mock_recommendation()
        mock_agent_instance = mock_restaurant_agent.return_value
        mock_agent_instance.ask.return_value = mock_result

        response = client.post("/recommend", json={"query": "best Swahili food in Kampala"})

        assert response.status_code == 200
        data = response.json()
        assert data["recommendation"]["neighborhood_searched"] == "Kampala"
        assert len(data["recommendation"]["recommended_spots"]) == 1
        assert data["recommendation"]["recommended_spots"][0]["name"] == "The Lamu House"

    def test_recommend_agent_raises_value_error(self, mock_restaurant_agent):
        mock_restaurant_agent.side_effect = ValueError("Missing API key")
        response = client.post("/recommend", json={"query": "best pizza"})

        assert response.status_code == 500
        assert response.json()["detail"] == "Missing API key"

    def test_recommend_agent_returns_none(self, mock_restaurant_agent):
        mock_agent_instance = mock_restaurant_agent.return_value
        mock_agent_instance.ask.return_value = None

        response = client.post("/recommend", json={"query": "best sushi"})

        assert response.status_code == 502
        assert response.json()["detail"] == "Agent returned no recommendation."
