"""End-to-end evals.

Drive the full stack — agent → tools → Nominatim/Foursquare — with the
external APIs mocked. Verifies the agent produces real-shaped output when
the tools return real-shaped data, and degrades cleanly when they fail.
"""

import json
from unittest.mock import MagicMock, patch

from agent.agent import RestaurantAgent
from agent.schema import RestaurantRecommendations

from .fixtures import mock_response, recommendation_json


class TestEndToEnd:
    def test_happy_path_with_mocked_tools(
        self, mock_env, mock_openai_client
    ):
        agent = RestaurantAgent()

        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[
                    MagicMock(
                        id="c1",
                        function=MagicMock(
                            name="search_restaurants_by_area",
                            arguments=json.dumps({"area": "Kololo"}),
                        ),
                    )
                ],
            ),
            mock_response(content=recommendation_json(neighborhood="Kololo")),
        ]

        with patch(
            "agent.agent.AVAILABLE_TOOLS",
            {
                "search_restaurants_by_area": lambda **kwargs: {
                    "results": [
                        {
                            "name": "Cafe Javas",
                            "location": "Kololo",
                            "categories": [{"name": "Italian Restaurant"}],
                            "rating": 4.4,
                        }
                    ]
                }
            },
        ):
            result = agent.ask("best restaurants in Kololo")

        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kololo"
        assert result.recommended_spots

    def test_foursquare_rate_limit_does_not_crash(
        self, mock_env, mock_openai_client
    ):
        agent = RestaurantAgent()

        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[
                    MagicMock(
                        id="c1",
                        function=MagicMock(
                            name="search_restaurants_by_area",
                            arguments=json.dumps({"area": "Nakawa"}),
                        ),
                    )
                ],
            ),
            mock_response(content=recommendation_json()),
        ]

        with patch(
            "agent.agent.AVAILABLE_TOOLS",
            {
                # Simulate Foursquare returning [] on a 429.
                "search_restaurants_by_area": lambda **kwargs: [],
            },
        ):
            result = agent.ask("restaurants in Nakawa")

        assert result is not None

    def test_nominatim_resolution_failure_does_not_crash(
        self, mock_env, mock_openai_client
    ):
        agent = RestaurantAgent()

        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[
                    MagicMock(
                        id="c1",
                        function=MagicMock(
                            name="search_restaurants_by_area",
                            arguments=json.dumps({"area": "NonexistentPlace"}),
                        ),
                    )
                ],
            ),
            mock_response(content=recommendation_json()),
        ]

        with patch(
            "agent.agent.AVAILABLE_TOOLS",
            {
                # Nominatim returned no coordinates → tool returns [].
                "search_restaurants_by_area": lambda **kwargs: [],
            },
        ):
            result = agent.ask("food in NonexistentPlace")

        assert result is not None

    def test_conversation_history_grows_per_ask(
        self, mock_env, mock_openai_client
    ):
        agent = RestaurantAgent()
        mock_openai_client.return_value.chat.completions.create.return_value = (
            mock_response(content=recommendation_json())
        )

        agent.ask("first query")
        first_len = len(agent.messages)

        agent.ask("second query")
        second_len = len(agent.messages)

        assert second_len > first_len
        # Each ask appends a user message.
        user_messages = [m for m in agent.messages if m["role"] == "user"]
        assert len(user_messages) == 2
