import json
from unittest.mock import MagicMock, patch

import pytest

from agent.agent import RestaurantAgent
from agent.schema import RestaurantRecommendations, RestaurantDetails


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
        yield


@pytest.fixture
def mock_openai_client():
    with patch("agent.agent.OpenAI") as MockOpenAI:
        yield MockOpenAI


@pytest.fixture
def mock_available_tools():
    with patch("agent.agent.AVAILABLE_TOOLS") as MockTools:
        yield MockTools


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


def test_restaurant_agent_init_raises_without_api_key():
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="OPENROUTER_API_KEY environment variable is not set."):
            RestaurantAgent()


def test_restaurant_agent_init_success(mock_env, mock_openai_client):
    agent = RestaurantAgent()
    assert agent.model_name == "meta-llama/llama-4-scout"
    assert len(agent.messages) == 1
    assert agent.messages[0]["role"] == "system"
    mock_openai_client.assert_called_once()


class TestExtractAndParseJson:
    def test_valid_json(self):
        agent = RestaurantAgent.__new__(RestaurantAgent)
        data = make_mock_recommendation().model_dump()
        raw = json.dumps(data)
        result = agent._extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kampala"

    def test_json_in_markdown_block(self):
        agent = RestaurantAgent.__new__(RestaurantAgent)
        data = make_mock_recommendation().model_dump()
        raw = f"```json\n{json.dumps(data)}\n```"
        result = agent._extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kampala"

    def test_json_missing_opening_brace(self):
        agent = RestaurantAgent.__new__(RestaurantAgent)
        data = make_mock_recommendation().model_dump()
        raw = json.dumps(data)[1:]
        result = agent._extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kampala"

    def test_json_missing_closing_brace(self):
        agent = RestaurantAgent.__new__(RestaurantAgent)
        data = make_mock_recommendation().model_dump()
        raw = json.dumps(data)[:-1]
        result = agent._extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)
        assert result.neighborhood_searched == "Kampala"

    def test_invalid_json_returns_none(self):
        agent = RestaurantAgent.__new__(RestaurantAgent)
        result = agent._extract_and_parse_json("not valid json {{{")
        assert result is None

    def test_none_input_returns_none(self):
        agent = RestaurantAgent.__new__(RestaurantAgent)
        assert agent._extract_and_parse_json(None) is None
        assert agent._extract_and_parse_json("") is None


class TestAsk:
    def test_ask_success(self, mock_env, mock_openai_client, mock_available_tools):
        mock_available_tools.__getitem__.side_effect = lambda key: lambda **kwargs: {"result": "ok"}
        mock_available_tools.__contains__.side_effect = lambda key: True

        mock_message = MagicMock()
        mock_message.content = json.dumps(make_mock_recommendation().model_dump())
        mock_message.tool_calls = None

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

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

        final_response = MagicMock()
        final_response.choices = [MagicMock(message=tool_response_msg)]

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

        final_response = MagicMock()
        final_response.choices = [MagicMock(message=tool_response_msg)]

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
        mock_message = MagicMock()
        mock_message.content = "completely invalid response"
        mock_message.tool_calls = None

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

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
