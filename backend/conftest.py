"""Pytest bootstrap.

Ensures the ``backend`` package directory is importable regardless of the
directory pytest is invoked from (e.g. ``pytest`` from the repo root vs.
``pytest`` from inside ``backend/``).
"""

import os
import sys
from unittest.mock import patch

import pytest

_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)


@pytest.fixture
def mock_env(monkeypatch):
    """Provide a fake ``OPENROUTER_API_KEY`` so agents can be constructed."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")


@pytest.fixture
def mock_openai_client():
    """Patch the OpenAI client constructor so no network call is made."""
    with patch("agent.agent.OpenAI") as mock_client:
        yield mock_client