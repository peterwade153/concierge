# Concierge-ai

A Restaurant Recommendation Agent, to recommend fine dining spots in specific neighborhood. 
Uses Nominatim to get Location Coordinates, and FourSquare to look up restaurants with those Coordinates in a given radius.

### Installation

1. Create and activate a virtual environment and Clone the project `https://github.com/peterwade153/concierge.git`

2. Move into the project folder
   ```
    cd concierge
   ```

3. Install dependencies 
   ```
    pip install -r requirements.txt
   ```

4. Create a `.env` file from the `.env.sample` file. 

5. Replace the variables in the sample file with the actual variables e.g. API KEY etc. Required generating a GEMINI_API_KEY via Google AI Studio @ https://aistudio.google.com/apikey or OPENROUTER_API_KEY


## Start Server
```bash
    python api/run.py
```
Post Request endpoint - `/recommend`

sample payload
``` json
   {
      "query": "Find me a good spot for Asian food around the Ntinda or Nakawa neighborhood."
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

## Run Tests
```bash
    pytest
```
