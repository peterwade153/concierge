import os 

from agent.openrouter_agent import RestaurantAgent as RA


if __name__ == "__main__":
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise ValueError("Please set your OPENROUTER_API_KEY environment variable.")

    concierge = RA()
    
    concierge.ask("Find me a good spot for Asian food around the Ntinda or Nakawa neighborhood.")
