# Task: Add a client-side timeout to the OpenAI client

## Issue

`backend/agent/agent.py:84-87` — the OpenAI client is constructed with no timeout:

```python
self.client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)
```

The OpenAI SDK defaults to no timeout. If the model is slow or the provider stalls, `chat.completions.create()` blocks indefinitely. Under load this exhausts worker threads and can hang the FastAPI process.

## Requirements

1. The `OpenAI` client must be constructed with an explicit `timeout`.
2. Default timeout: **30 seconds** per request.
3. On timeout, the request must surface as a handled exception — `ask()` already has a broad `except Exception` that returns `None`, so a `openai.APITimeoutError` (or the underlying `requests` timeout) is caught and converted to a 502, consistent with other failures.
4. The timeout must be configurable via environment variable `OPENROUTER_REQUEST_TIMEOUT` (integer seconds), defaulting to 30.
5. No change to the client's `base_url` or `api_key` configuration.
6. Logging must record that a timeout occurred.

## Checklist

- [ ] The `OpenAI` constructor is called with a `timeout` argument
- [ ] A mocked client that times out causes `ask()` to return `None` (not hang)
- [ ] `OPENROUTER_REQUEST_TIMEOUT` env var overrides the default
- [ ] Default value is 30 when the env var is unset
- [ ] A timeout is logged
- [ ] `ruff check backend` passes
- [ ] `pytest` passes (existing tests intact)

## Files to change

- `backend/agent/agent.py` — add `timeout` to the `OpenAI()` constructor
- `backend/tests/evals/test_error_resilience.py` — add a test for timeout handling