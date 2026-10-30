# Task: Fix `filter_by_cuisine` tool

## Issue

`backend/agent/tools.py:26-36` — the `filter_by_cuisine` tool is non-functional and semantically wrong.

**Bug 1 — crash on call.** `extract_cuisines(place_data: dict)` calls `place_data.get("categories", [])`, but `filter_by_cuisine` passes a *list* of restaurants, not a single place dict. A list has no `.get` method, so the tool raises `AttributeError`. The agent's broad `except Exception` in `ask()` swallows it and returns `None`, which the API turns into a 502. Any query that causes the model to invoke `filter_by_cuisine` fails.

**Bug 2 — wrong semantics even if it ran.** The current check is:

```python
cuisines = extract_cuisines(restaurants)          # flattened list across ALL restaurants
filtered = [r for r in restaurants if cuisine in cuisines]
```

`cuisine in cuisines` tests membership in the *aggregate* list. If restaurant A serves Italian and restaurant B serves Pizza, filtering by "Italian" returns **both** A and B. The correct behavior is: return only restaurants whose *own* cuisine list contains the match.

## Requirements

1. `filter_by_cuisine` must not crash when given a list of restaurant dicts.
2. Filtering must be per-restaurant: a restaurant is included only if its own extracted cuisines contain the requested cuisine.
3. Matching should be case-insensitive and tolerant of minor wording differences (e.g. "Italian" matches "Italian Restaurant").
4. The tool must return a list, never raise, when given valid input.
5. Empty input returns an empty list rather than crashing.
6. The function signature and the `TOOL_SCHEMAS` entry for `filter_by_cuisine` must remain unchanged.

## Checklist

- [ ] `filter_by_cuisine([{"name": "A", "categories": [{"name": "Italian Restaurant"}]}], "Italian")` returns `[A]`
- [ ] `filter_by_cuisine([A, B], "Italian")` returns only restaurants whose own cuisines include Italian
- [ ] Calling the tool through the agent loop (mocked client) does not raise `AttributeError`
- [ ] A cuisine query that triggers `filter_by_cuisine` returns a 200, not a 502
- [ ] Empty restaurant list returns `[]`
- [ ] Case-insensitive: `"italian"` matches `"Italian Restaurant"`
- [ ] `TOOL_SCHEMAS["filter_by_cuisine"]` is unchanged
- [ ] `ruff check backend` passes
- [ ] `pytest` passes (existing tests intact)

## Files to change

- `backend/agent/tools.py` — rewrite `filter_by_cuisine` body
- `backend/tests/evals/test_tool_calling.py` — add a test exercising `filter_by_cuisine` through the agent loop