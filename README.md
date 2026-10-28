# Concierge-ai

A Restaurant Recommendation Agent, to recommend fine dining spots in specific neighborhood. 
Uses Nominatim to get Location Coordinates, and FourSquare to look up restaurants with those Coordinates in a given radius.

![Dashboard](<Screenshot 2026-10-28 at 16.05.29.png>)

### Installation

1. Create and activate a virtual environment and Clone the project `https://github.com/peterwade153/concierge.git`

2. Move into the project folder
   ```
    cd concierge
   ```

3. Install dependencies 
   ```
    pip install -r backend/requirements.txt
   ```

4. Create a `.env` file from the `.env.sample` file. 

5. Replace the variables in the sample file with the actual variables e.g. API KEY etc. Required generating a GEMINI_API_KEY via Google AI Studio @ https://aistudio.google.com/apikey or OPENROUTER_API_KEY


## Start Server
```bash
    python backend/api/run.py
```
Post Request endpoint - `/api/recommend`

sample payload
``` json
   {
      "query": "Find me a good spot for Asian food around the Kololo neighborhood."
   }
```

sample response
``` json
{
    "recommendation": {
        "neighborhood_searched": "Kololo",
        "recommended_spots": [
            {
                "name": "Mona Lisa Restaurant",
                "location": "Kololo, Kampala",
                "cuisine": [
                    "Italian",
                    "Continental"
                ],
                "price_range": "UGX 50,000 - 100,000",
                "rating": 4.5,
                "specialty": "Pasta and Pizza"
            },
            {
                "name": "The Italian Kitchen",
                "location": "Kololo, Kampala",
                "cuisine": [
                    "Italian"
                ],
                "price_range": "UGX 30,000 - 70,000",
                "rating": 4.2,
                "specialty": "Homemade pasta and wood-fired pizzas"
            }
        ],
        "summary_verdict": "Enjoy authentic Italian cuisine at Mona Lisa Restaurant or The Italian Kitchen in Kololo."
    }
}

```

## Frontend (React SPA)

A small Vite + React + TypeScript + Tailwind UI lives in `frontend/`.

### Run locally
```bash
cd frontend
npm install
npm run dev      # http://localhost:5173 — API is proxied to the backend on :8000
npm run typecheck
```

### Build for production
```bash
cd frontend
npm run build    # outputs dist/
```

### Run tests
```bash
cd frontend
npm test
```

## Docker

The stack is split into two containers: a Python backend and an nginx-served frontend.

### Run with Docker Compose
```bash
cp .env.sample .env   # then fill in OPENROUTER_API_KEY and FOURSQUARE_API_KEY
docker compose up --build
```
Open `http://localhost` — the frontend proxies `/api/` requests to the backend.

## Run API Tests
```bash
    pytest
```
