"""JSON repair evals.

Validates ``extract_and_parse_json`` against the ways LLMs commonly
misformat JSON. The function handles a curated set of repairs; the
negative tests below document known limitations so future work can
tell when the coverage has expanded.
"""

from agent.agent import extract_and_parse_json
from agent.schema import RestaurantRecommendations

from .fixtures import recommendation_json


class TestJsonRepair:
    def test_valid_json_passes_through(self):
        raw = recommendation_json()
        result = extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)

    def test_markdown_json_fence_stripped(self):
        raw = f"```json\n{recommendation_json()}\n```"
        result = extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)

    def test_bare_markdown_fence_stripped(self):
        raw = f"```\n{recommendation_json()}\n```"
        result = extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)

    def test_missing_opening_brace_repaired(self):
        raw = recommendation_json()[1:]  # drop leading '{'
        result = extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)

    def test_missing_closing_brace_repaired(self):
        raw = recommendation_json()
        if raw.endswith("}"):
            raw = raw[:-1]
        result = extract_and_parse_json(raw)
        assert isinstance(result, RestaurantRecommendations)

    # --- Known limitations (documented, not silently passing) ---

    def test_both_braces_missing_is_known_limitation(self):
        """Dropping both braces leaves content the repairer can't recover."""
        raw = recommendation_json()[1:-1]
        assert extract_and_parse_json(raw) is None

    def test_leading_prose_is_known_limitation(self):
        """Prose before the JSON defeats the brace-repair heuristic."""
        raw = "Here is the recommendation:\n\n" + recommendation_json()
        assert extract_and_parse_json(raw) is None

    def test_trailing_prose_is_known_limitation(self):
        """Prose after the JSON defeats the brace-repair heuristic."""
        raw = recommendation_json() + "\n\nLet me know if you need more."
        assert extract_and_parse_json(raw) is None

    def test_markdown_fence_with_surrounding_text_is_known_limitation(self):
        """Fences not at the very start/end are not stripped."""
        raw = "Sure! ```json\n" + recommendation_json() + "\n``` Hope this helps."
        assert extract_and_parse_json(raw) is None

    # --- Negative cases ---

    def test_garbage_returns_none(self):
        assert extract_and_parse_json("totally not json {{{") is None

    def test_none_input_returns_none(self):
        assert extract_and_parse_json(None) is None

    def test_empty_string_returns_none(self):
        assert extract_and_parse_json("") is None

    def test_whitespace_only_returns_none(self):
        assert extract_and_parse_json("   \n\t  ") is None