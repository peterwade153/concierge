# Task: Add tool-call depth limit to the agent loop

## Issue

`backend/agent/agent.py:127` — the tool-call loop has no termination guard:

```python
while response_message.tool_calls:
    ...
    response = self.client.chat.completions.create(...)
    response_message = response.choices[0].message
```

If the model keeps requesting tools (e.g. it calls `search_restaurants_by_area`, gets results, then calls it again with a slightly different area, and so on), the loop runs forever. Each iteration is a paid API call, so this is both a correctness and a cost problem. There is no `max_steps` cap.

## Requirements

1. The agent loop must stop after a bounded number of tool-call iterations.
2. When the limit is reached, `ask()` must return `None` (so the API returns 502) rather than looping or crashing.
3. The limit must be configurable without editing source code — a module-level constant is acceptable.
4. A sensible default: **10 tool-call steps** per `ask()` invocation.
5. The limit must be observable: log a warning when it is hit, including the query and step count.
6. Existing behavior for the normal case (loop exits because the model returns text) must be unchanged.

## Checklist

- [ ] A mocked client that returns tool calls forever terminates after ≤ 10 iterations
- [ ] `ask()` returns `None` when the limit is hit
- [ ] A warning is logged when the limit is hit
- [ ] A normal two-step tool loop still returns a valid recommendation
- [ ] The limit constant is defined once at module level, not hardcoded inline
- [ ] `ruff check backend` passes
- [ ] `pytest` passes (existing tests intact)

## Files to change

- `backend/agent/agent.py` — add `MAX_TOOL_STEPS` constant and guard the loop
- `backend/tests/evals/test_tool_calling.py` — add a test for the limit being hit