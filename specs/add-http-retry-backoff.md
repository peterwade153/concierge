# Task: Add retry with backoff to the HTTP tools

## Issue

`backend/agent/utils/nominatim.py` and `backend/agent/utils/foursquare.py` make single-attempt HTTP requests with no retry logic.

- **Nominatim** is explicitly rate-limited by OpenStreetMap and expects clients to back off on 429. The current code returns `None` immediately on any error, so a transient 429 or timeout causes the whole recommendation to fail.
- **Foursquare** has the same gap: 429 returns `[]`, but timeouts and transient 5xx errors also fail immediately.

The agent's `ask()` catches the resulting `None`/empty output and returns a 502. Under real usage — rate limits, brief network blips, upstream hiccups — this happens more often than it should.

## Requirements

1. Both `get_location_coordinates` and `search_foursquare_restaurants` must retry on transient failures.
2. Transient failures include: `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, HTTP 429, and HTTP 5xx.
3. Retries must use **exponential backoff** with jitter, starting at ~1s and capping at ~8s.
4. Maximum **3 attempts** total (1 initial + 2 retries).
5. Non-transient failures must not be retried: HTTP 4xx (other than 429) fails immediately.
6. The function signatures must remain unchanged.
7. Retry state must be observable via logging, not silent.
8. If all attempts are exhausted, the function returns its failure sentinel (`None` for Nominatim, `[]` for Foursquare) — behavior identical to today's failure path, just more resilient on the way there.
9. No new external dependency unless it is already in `backend/requirements.txt`. Prefer a small hand-rolled retry loop over adding `tenacity` if it is not present.

## Checklist

- [ ] Nominatim: a mocked 429 followed by 200 succeeds on the second attempt
- [ ] Nominatim: a mocked `Timeout` followed by 200 succeeds on the second attempt
- [ ] Nominatim: a persistent 429 returns `None` after 3 attempts
- [ ] Foursquare: a mocked `Timeout` followed by 200 succeeds on the second attempt
- [ ] Foursquare: a persistent 500 returns `[]` after 3 attempts
- [ ] A non-transient 4xx (e.g. 404) fails immediately with no retry
- [ ] Backoff duration increases between attempts (exponential)
- [ ] Function signatures unchanged
- [ ] `ruff check backend` passes
- [ ] `pytest` passes (existing tests intact)

## Files to change

- `backend/agent/utils/nominatim.py` — add retry loop
- `backend/agent/utils/foursquare.py` — add retry loop
- `backend/tests/evals/test_e2e.py` — add tests for transient-failure recovery