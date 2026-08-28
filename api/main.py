from fastapi import FastAPI, HTTPException

from agent.agent import RestaurantAgent
from api.schema import RecommendRequest, RecommendResponse


app = FastAPI(title="Concierge API", version="1.0.0")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Concierge API"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    try:
        agent = RestaurantAgent()
        result = agent.ask(request.query)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        raise HTTPException(
            status_code=502,
            detail="Agent returned no recommendation."
        )

    return RecommendResponse(recommendation=result)
