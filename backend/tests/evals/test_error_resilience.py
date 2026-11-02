"""Error-resilience evals.

The agent must degrade gracefully: never raise out of ``ask()``, return
``None`` on parse failure, and fail fast at construction when credentials
are missing.
"""

from unittest.mock import patch

import pytest

from agent.agent import RestaurantAgent
from agent.utils.client import DEFAULT_REQUEST_TIMEOUT_SECONDS

from .fixtures import mock_response


class TestErrorResilience:
    def test_ask_returns_none_on_api_exception(
        self, mock_env, mock_openai_client
    ):
        agent = RestaurantAgent()
        mock_openai_client.return_value.chat.completions.create.side_effect = Exception("API Error")
        assert agent.ask("best pasta") is None

    def test_ask_returns_none_on_timeout(self, mock_env, mock_openai_client):
        """A timed-out request must surface as ``None``, not hang."""
        agent = RestaurantAgent()
        mock_openai_client.return_value.chat.completions.create.side_effect = TimeoutError("request timed out")
        assert agent.ask("best pasta") is None

    def test_ask_returns_none_on_parse_failure(
        self, mock_env, mock_openai_client
    ):
        agent = RestaurantAgent()
        mock_openai_client.return_value.chat.completions.create.return_value = (
            mock_response(content="invalid json response")
        )
        assert agent.ask("best burgers") is None

    def test_ask_returns_none_on_empty_response(
        self, mock_env, mock_openai_client
    ):
        agent = RestaurantAgent()
        mock_openai_client.return_value.chat.completions.create.return_value = (
            mock_response(content=None)
        )
        assert agent.ask("best noodles") is None

    def test_init_raises_without_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
                RestaurantAgent()

    def test_init_does_not_require_foursquare_key(self, mock_env, mock_openai_client):
        """FOURSQUARE_API_KEY is checked lazily inside the tool, not at init."""
        agent = RestaurantAgent()
        assert agent.model_name

    def test_init_success_sets_model_and_messages(
        self, mock_env, mock_openai_client
    ):
        agent = RestaurantAgent()
        assert agent.model_name
        assert len(agent.messages) == 1
        assert agent.messages[0]["role"] == "system"

    def test_init_client_configured_with_openrouter_base_url(
        self, mock_env, mock_openai_client
    ):
        RestaurantAgent()
        _, kwargs = mock_openai_client.call_args
        assert kwargs["base_url"] == "https://openrouter.ai/api/v1"
        assert kwargs["api_key"] == "test-key"
        assert kwargs["timeout"] == DEFAULT_REQUEST_TIMEOUT_SECONDS

    def test_init_uses_default_timeout_when_env_unset(
        self, mock_env, mock_openai_client, monkeypatch
    ):
        """With OPENROUTER_REQUEST_TIMEOUT unset, the default applies."""
        monkeypatch.delenv("OPENROUTER_REQUEST_TIMEOUT", raising=False)
        RestaurantAgent()
        _, kwargs = mock_openai_client.call_args
        assert kwargs["timeout"] == float(DEFAULT_REQUEST_TIMEOUT_SECONDS)

    def test_init_uses_env_timeout_when_set(
        self, mock_env, mock_openai_client
    ):
        with patch.dict(
            "os.environ", {"OPENROUTER_REQUEST_TIMEOUT": "12"}, clear=False
        ):
            RestaurantAgent()
            _, kwargs = mock_openai_client.call_args
            assert kwargs["timeout"] == 12.0

    def test_init_falls_back_to_default_on_invalid_env(
        self, mock_env, mock_openai_client
    ):
        with patch.dict(
            "os.environ", {"OPENROUTER_REQUEST_TIMEOUT": "not-a-number"}, clear=False
        ):
            RestaurantAgent()
            _, kwargs = mock_openai_client.call_args
            assert kwargs["timeout"] == float(DEFAULT_REQUEST_TIMEOUT_SECONDS)
