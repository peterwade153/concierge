import os 

from agent.openrouter_agent import RestaurantAgent as RA


if __name__ == "__main__":
    # Ensure GEMINI_API_KEY environment variable is set before running
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("Please set your GEMINI_API_KEY environment variable.")

    concierge = RA()
    
    # Execution Test Case: Multi-turn filtering logic
    concierge.ask("Find me a good spot for Asian food around the Ntinda or Nakawa neighborhood.")
