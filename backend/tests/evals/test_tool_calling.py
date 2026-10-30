"""Tool-calling evals.

The agent's core behavior is delegating to ``AVAILABLE_TOOLS`` and looping
until the model returns a final text response. These tests mock the OpenAI
client and verify the loop drives the right tools and terminates.
"""

from unittest.mock import patch

from agent.agent import RestaurantAgent

from .fixtures import mock_response, mock_tool_call, recommendation_json


def _make_agent(mock_openai_client):
    return RestaurantAgent()


class TestToolCalling:
    def test_search_tool_invoked_for_neighborhood_query(
        self, mock_env, mock_openai_client
    ):
        agent = _make_agent(mock_openai_client)
        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[
                    mock_tool_call(
                        "search_restaurants_by_area", {"area": "Kololo"}
                    )
                ],
            ),
            mock_response(content=recommendation_json()),
        ]

        with patch(
            "agent.agent.AVAILABLE_TOOLS",
            {
                "search_restaurants_by_area": lambda **kwargs: {
                    "results": [{"name": "X"}]
                }
            },
        ):
            result = agent.ask("best restaurants in Kololo")

        assert result is not None
        assert mock_openai_client.return_value.chat.completions.create.call_count == 2

    def test_cuisine_filter_invoked_when_food_type_named(
        self, mock_env, mock_openai_client
    ):
        agent = _make_agent(mock_openai_client)
        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[
                    mock_tool_call(
                        "search_restaurants_by_area", {"area": "Nakawa"}
                    ),
                    mock_tool_call(
                        "filter_by_cuisine",
                        {"restaurants": [{"name": "X"}], "cuisine": "Italian"},
                    ),
                ],
            ),
            mock_response(content=recommendation_json()),
        ]

        with patch(
            "agent.agent.AVAILABLE_TOOLS",
            {
                "search_restaurants_by_area": lambda **kwargs: {"results": []},
                "filter_by_cuisine": lambda **kwargs: [],
            },
        ):
            result = agent.ask("Italian food in Nakawa")

        assert result is not None
        # Two tool calls in one turn → one initial request + one follow-up.
        assert mock_openai_client.return_value.chat.completions.create.call_count == 2

    def test_tool_loop_terminates_with_final_text(
        self, mock_env, mock_openai_client
    ):
        agent = _make_agent(mock_openai_client)
        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[mock_tool_call("search_restaurants_by_area", {"area": "X"})],
            ),
            mock_response(content=recommendation_json()),
        ]

        with patch(
            "agent.agent.AVAILABLE_TOOLS",
            {"search_restaurants_by_area": lambda **kwargs: {}},
        ):
            result = agent.ask("anything")

        assert result is not None

    def test_unavailable_tool_yields_error_payload(
        self, mock_env, mock_openai_client
    ):
        agent = _make_agent(mock_openai_client)
        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[mock_tool_call("ghost_tool", {})],
            ),
            mock_response(content=recommendation_json()),
        ]

        result = agent.ask("best sushi")
        assert result is not None

        tool_messages = [m for m in agent.messages if m["role"] == "tool"]
        assert tool_messages
        assert "error" in tool_messages[0]["content"]

    def test_tool_call_id_propagated_to_tool_message(
        self, mock_env, mock_openai_client
    ):
        agent = _make_agent(mock_openai_client)
        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[mock_tool_call("search_restaurants_by_area", {"area": "X"}, call_id="abc")],
            ),
            mock_response(content=recommendation_json()),
        ]

        with patch(
            "agent.agent.AVAILABLE_TOOLS",
            {"search_restaurants_by_area": lambda **kwargs: {}},
        ):
            agent.ask("query")

        tool_messages = [m for m in agent.messages if m["role"] == "tool"]
        assert tool_messages[0]["tool_call_id"] == "abc"

    def test_multiple_tool_calls_in_one_turn(
        self, mock_env, mock_openai_client
    ):
        agent = _make_agent(mock_openai_client)
        mock_openai_client.return_value.chat.completions.create.side_effect = [
            mock_response(
                content=None,
                tool_calls=[
                    mock_tool_call("search_restaurants_by_area", {"area": "A"}, "c1"),
                    mock_tool_call("search_restaurants_by_area", {"area": "B"}, "c2"),
                ],
            ),
            mock_response(content=recommendation_json()),
        ]

        with patch(
            "agent.agent.AVAILABLE_TOOLS",
            {"search_restaurants_by_area": lambda **kwargs: {}},
        ):
            result = agent.ask("compare A and B")

        assert result is not None
        tool_messages = [m for m in agent.messages if m["role"] == "tool"]
        assert len(tool_messages) == 2
