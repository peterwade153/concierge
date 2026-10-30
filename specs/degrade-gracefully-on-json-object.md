# Task: Make `response_format` degrade gracefully

## Issue

`backend/agent/agent.py:118` — every `chat.completions.create` call passes `response_format={"type": "json_object"}`:

```python
response = self.client.chat.completions.create(
    model=self.model_name,
    messages=self.messages,
    tools=self.tools,
    temperature=0.1,
    response_format={"type": "json_object"},
)
```

This constraint is sent to OpenRouter, which forwards it to the underlying model. Not every model supports `json_object` mode. When a model rejects it, the request fails outright and `ask()` returns `None` → 502.

The agent already has robust JSON parsing in `extract_and_parse_json` (markdown fence stripping, brace repair), so the `response_format` constraint is a *hint*, not a requirement. The failure mode is worse than not sending it.

## Requirements

1. The initial request must send `response_format={"type": "json_object"}` (current behavior — models that support it get structured output).
2. If the model rejects `json_object` (or the provider returns an error attributable to it), the agent must retry the request **without** `response_format`.
3. The retry must use the same messages, tools, and temperature.
4. If the no-constraint request also fails, `ask()` returns `None` (current failure path).
5. The retry must be a single attempt — no cascading retries.
6. The change must not affect the tool-call loop: only the final text response needs the fallback, and the fallback applies to all `create()` calls in the loop uniformly for simplicity.
7. Logging must record when the fallback is triggered.

## Checklist

- [ ] A mocked client that raises on `json_object` mode succeeds on a retry without `response_format`
- [ ] The retry request omits `response_format` (verified via mock assertion)
- [ ] A mocked client that raises on both attempts returns `None`
- [ ] A mocked client that accepts `json_object` makes exactly one call (no unnecessary retry)
- [ ] The fallback is logged
- [ ] A normal tool-loop + final response still returns a valid recommendation
- [ ] `ruff check backend` passes
- [ ] `pytest` passes (existing tests intact)

## Files to change

- `backend/agent/agent.py` — wrap `create()` calls with the fallback
- `backend/tests/evals/test_tool_calling.py` — add a test for the fallback path