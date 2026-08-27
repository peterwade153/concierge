# Concierge

A Local Restaurant Recommendation Agent, to recommend fine dining spots in specific neighborhood.

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
Post Request endpoint - /recommend


sample payload
``` json
   {
      "query": "Find me a good spot for Asian food around the Ntinda or Nakawa neighborhood."
   }
```