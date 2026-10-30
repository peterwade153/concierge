"""Output contract evals.

Validates that the agent's final response always conforms to the
``RestaurantRecommendations`` schema — the invariant the whole UI and API
depend on. These tests are deterministic and require no network access.
"""

import json

import pytest
from pydantic import ValidationError

from agent.schema import RestaurantRecommendations

from .fixtures import make_recommendation, recommendation_json


class TestOutputContract:
    """The agent must always return a schema-valid object or ``None``."""

    def test_full_schema_parses(self):
        result = make_recommendation()
        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kampala"
        assert len(result.recommended_spots) == 1

    def test_required_fields_present(self):
        spot = make_recommendation().recommended_spots[0]
        assert spot.name
        assert spot.location
        assert isinstance(spot.cuisine, list)

    def test_optional_fields_can_be_none(self):
        spot = make_recommendation(
            spots=[
                {
                    "name": "Barebones",
                    "location": "Nowhere",
                    "cuisine": [],
                    "price_range": None,
                    "rating": None,
                    "specialty": None,
                }
            ]
        ).recommended_spots[0]

        assert spot.price_range is None
        assert spot.rating is None
        assert spot.specialty is None

    def test_empty_recommendation_list_is_valid(self):
        result = make_recommendation(spots=[])
        assert result.recommended_spots == []

    def test_cuisine_list_must_not_be_none(self):
        with pytest.raises(ValidationError):
            RestaurantRecommendations(
                neighborhood_searched="X",
                recommended_spots=[
                    {
                        "name": "Bad",
                        "location": "St",
                        "cuisine": None,
                    }
                ],
                summary_verdict="v",
            )

    def test_response_matches_api_contract(self):
        """The shape the frontend expects: ``recommendation`` wrapper."""
        data = json.loads(recommendation_json())
        assert "recommendation" not in data  # raw agent output has no wrapper
        assert "neighborhood_searched" in data
        assert "recommended_spots" in data
        assert "summary_verdict" in data
