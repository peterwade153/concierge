"""Shared fixtures and helpers for the eval suite.

These are intentionally lightweight so the evals run without any network
access or real API keys — every external dependency is mocked.
"""

import json
from typing import Any

from agent.schema import RestaurantDetails, RestaurantRecommendations


def make_recommendation(
    *,
    neighborhood: str = "Kampala",
    spots: list[dict[str, Any]] | None = None,
    verdict: str = "A great test recommendation.",
) -> RestaurantRecommendations:
    """Build a ``RestaurantRecommendations`` with sensible defaults."""
    if spots is None:
        spots = [
            {
                "name": "Test Restaurant",
                "location": "123 Test St",
                "cuisine": ["Test Cuisine"],
                "price_range": "UGX 10,000",
                "rating": 4.0,
                "specialty": "Test specialty dish.",
            }
        ]

    parsed_spots = [RestaurantDetails(**spot) for spot in spots]
    return RestaurantRecommendations(
        neighborhood_searched=neighborhood,
        recommended_spots=parsed_spots,
        summary_verdict=verdict,
    )


def recommendation_json(**kwargs: Any) -> str:
    """Serialize a recommendation to a JSON string, as the LLM would emit it."""
    return json.dumps(make_recommendation(**kwargs).model_dump())


def mock_response(
    content: str,
    tool_calls: list[Any] | None = None,
) -> Any:
    """Build a fake OpenAI chat-completion response.

    Mirrors the shape the agent reads: ``response.choices[0].message`` with
    ``content`` and ``tool_calls`` attributes.
    """
    from unittest.mock import MagicMock

    message = MagicMock()
    message.content = content
    message.tool_calls = tool_calls

    choice = MagicMock()
    choice.message = message

    response = MagicMock()
    response.choices = [choice]
    response.usage = None
    return response


def mock_tool_call(
    tool_name: str,
    arguments: dict[str, Any],
    call_id: str = "call_123",
) -> Any:
    """Build a fake tool-call object the agent loop iterates over."""
    from unittest.mock import MagicMock

    function = MagicMock()
    function.name = tool_name
    function.arguments = json.dumps(arguments)

    tool_call = MagicMock()
    tool_call.id = call_id
    tool_call.function = function
    return tool_call