from fastapi import FastAPI, HTTPException

from agent.agent import RestaurantAgent
from api.schema import RecommendRequest, RecommendResponse

app = FastAPI(title="Concierge API", version="1.0.0")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Concierge API"}


_cache: dict[str, object] = {}
_CACHE_MAXSIZE = 128


def get_cached_recommendation(query: str):
    """Run the agent for a query and cache successful results.

    Only non-``None`` results are cached, so a transient failure (rate
    limit, network blip) is retryable instead of becoming a permanent
    502. Cache is a plain dict with simple FIFO eviction; ``lru_cache``
    is unsuitable because it memoizes ``None`` as well.
    """
    cached = _cache.get(query)
    if cached is not None:
        return cached

    agent = RestaurantAgent()
    result = agent.ask(query)

    if result is not None:
        if len(_cache) >= _CACHE_MAXSIZE:
            _cache.pop(next(iter(_cache)))
        _cache[query] = result

    return result


@app.post("/api/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    try:
        normalized_query = request.query.strip().lower()
        result = get_cached_recommendation(normalized_query)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    if result is None:
        raise HTTPException(
            status_code=502,
            detail="Agent returned no recommendation."
        )

    return RecommendResponse(recommendation=result)
