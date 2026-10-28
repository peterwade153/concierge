import json
from unittest.mock import MagicMock, patch

import pytest

from agent.agent import RestaurantAgent, extract_and_parse_json
from agent.schema import RestaurantRecommendations, RestaurantDetails


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")


@pytest.fixture
def mock_openai_client():
    with patch("agent.agent.OpenAI") as MockOpenAI:
        yield MockOpenAI


def make_mock_recommendation():
    return RestaurantRecommendations(
        neighborhood_searched="Kampala",
        recommended_spots=[
            RestaurantDetails(
                name="Test Restaurant",
                location="123 Test St",
                cuisine=["Test Cuisine"],
                price_range="UGX 10,000",
                rating=4.0,
                specialty="Test specialty dish.",
            )
        ],
        summary_verdict="A great test recommendation.",
    )


class TestRestaurantAgent:
    # Initialization Tests
    def test_init_raises_without_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="OPENROUTER_API_KEY environment variable is not set."):
                RestaurantAgent()

    def test_init_success(self, mock_env, mock_openai_client):
        agent = RestaurantAgent()
        assert agent.model_name == "meta-llama/llama-4-scout"
        assert len(agent.messages) == 1
        assert agent.messages[0]["role"] == "system"
        mock_openai_client.assert_called_once_with(
            base_url="https://openrouter.ai/api/v1",
            api_key="test-key",
        )

    # JSON Parsing Tests
    def test_extract_and_parse_valid_json(self):
        data = make_mock_recommendation().model_dump()
        raw = json.dumps(data)
        result = extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kampala"

    def test_extract_and_parse_json_in_markdown_block(self):
        data = make_mock_recommendation().model_dump()
        raw = f"```json\n{json.dumps(data)}\n```"
        result = extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kampala"

    def test_extract_and_parse_malformed_json_fallback(self):
        data = make_mock_recommendation().model_dump()
        
        raw_missing_brace = json.dumps(data)[1:]
        result = extract_and_parse_json(raw_missing_brace)
        assert isinstance(result, RestaurantRecommendations)

    def test_extract_and_parse_invalid_json_returns_none(self):
        assert extract_and_parse_json("not valid json {{{") is None

    def test_extract_and_parse_none_and_empty_input_returns_none(self):
        assert extract_and_parse_json(None) is None
        assert extract_and_parse_json("") is None

    # Agent Query Execution (Ask) Tests
    def test_ask_success(self, mock_env, mock_openai_client):
        mock_message = MagicMock()
        mock_message.content = json.dumps(make_mock_recommendation().model_dump())
        mock_message.tool_calls = None

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock(choices=[mock_choice])

        mock_client_instance = mock_openai_client.return_value
        mock_client_instance.chat.completions.create.return_value = mock_response

        agent = RestaurantAgent()
        result = agent.ask("best Swahili food in Kampala")

        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kampala"
        assert len(agent.messages) == 3
        assert agent.messages[-1]["role"] == "assistant"

    def test_ask_tool_call_loop(self, mock_env, mock_openai_client):
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "search_restaurants"
        mock_tool_call.function.arguments = '{"query": "test"}'
        mock_tool_call.id = "call_123"

        tool_response_msg = MagicMock()
        tool_response_msg.content = json.dumps(make_mock_recommendation().model_dump())
        tool_response_msg.tool_calls = None

        final_response = MagicMock(choices=[MagicMock(message=tool_response_msg)])

        mock_client_instance = mock_openai_client.return_value
        mock_client_instance.chat.completions.create.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(tool_calls=[mock_tool_call], content=None))]),
            final_response,
        ]

        with patch("agent.agent.AVAILABLE_TOOLS", {"search_restaurants": lambda **kwargs: {"results": []}}):
            agent = RestaurantAgent()
            result = agent.ask("best pizza")

        assert isinstance(result, RestaurantRecommendations)
        assert mock_client_instance.chat.completions.create.call_count == 2
        assert any(msg["role"] == "tool" for msg in agent.messages)

    def test_ask_unavailable_tool(self, mock_env, mock_openai_client):
        mock_tool_call = MagicMock()
        mock_tool_call.function.name = "unknown_tool"
        mock_tool_call.function.arguments = "{}"
        mock_tool_call.id = "call_456"

        tool_response_msg = MagicMock()
        tool_response_msg.content = json.dumps(make_mock_recommendation().model_dump())
        tool_response_msg.tool_calls = None

        final_response = MagicMock(choices=[MagicMock(message=tool_response_msg)])

        mock_client_instance = mock_openai_client.return_value
        mock_client_instance.chat.completions.create.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(tool_calls=[mock_tool_call], content=None))]),
            final_response,
        ]

        agent = RestaurantAgent()
        result = agent.ask("best sushi")

        assert isinstance(result, RestaurantRecommendations)
        tool_msg = [msg for msg in agent.messages if msg["role"] == "tool"][0]
        assert "error" in json.loads(tool_msg["content"])

    def test_ask_parsing_failure_returns_none(self, mock_env, mock_openai_client):
        mock_message = MagicMock(content="invalid json response", tool_calls=None)
        mock_response = MagicMock(choices=[MagicMock(message=mock_message)])

        mock_client_instance = mock_openai_client.return_value
        mock_client_instance.chat.completions.create.return_value = mock_response

        agent = RestaurantAgent()
        result = agent.ask("best burgers")

        assert result is None

    def test_ask_api_exception_returns_none(self, mock_env, mock_openai_client):
        mock_client_instance = mock_openai_client.return_value
        mock_client_instance.chat.completions.create.side_effect = Exception("API Error")

        agent = RestaurantAgent()
        result = agent.ask("best pasta")

        assert result is None
