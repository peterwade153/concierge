# Task: Validate and bound user query input

## Issue

`backend/agent/agent.py:111` — the user query is appended to the message history and sent to the LLM with no validation:

```python
self.messages.append({"role": "user", "content": user_query})
```

Problems:

- **Empty/whitespace queries** reach the model. The model may return a recommendation for a default area or, worse, hallucinate — instead of being rejected cheaply at the boundary.
- **Overly long queries** are a token-cost risk with no benefit. A 10,000-character query burns prompt tokens before any tooling happens.
- **The API endpoint** (`backend/api/main.py:42`) only normalizes casing (`strip().lower()`); it does not reject bad input, so the cache key can be `"   "` or a huge string.

## Requirements

1. `RestaurantAgent.ask()` must reject empty or whitespace-only queries by returning `None` immediately — no API call made.
2. `ask()` must reject queries longer than a configurable limit (default **500 characters**) by returning `None` immediately.
3. The API endpoint must return a **400** with a clear detail message for both cases, rather than 500/502.
4. The cache key normalization (`strip().lower()`) must remain unchanged for valid queries.
5. Rejection must be observable via logging at `INFO` level.
6. No change to the `ask()` return type or the `/api/recommend` response shape for the success path.

## Checklist

- [ ] `ask("")` returns `None` without calling the OpenAI client
- [ ] `ask("   ")` returns `None` without calling the OpenAI client
- [ ] `ask("x" * 501)` returns `None` without calling the OpenAI client
- [ ] `ask("x" * 500)` is accepted (at the boundary, inclusive)
- [ ] `POST /api/recommend {"query": ""}` returns 400
- [ ] `POST /api/recommend {"query": "   "}` returns 400
- [ ] `POST /api/recommend {"query": "x" * 501}` returns 400
- [ ] The 400 response body has a `detail` field with a human-readable message
- [ ] A valid query still returns 200 and is cached as before
- [ ] `ruff check backend` passes
- [ ] `pytest` passes (existing tests intact)

## Files to change

- `backend/agent/agent.py` — add validation at the top of `ask()`
- `backend/api/main.py` — map the rejection to a 400 HTTPException
- `backend/tests/evals/test_error_resilience.py` — add tests for empty/long query rejection