import os 

from agent.openrouter_agent import RestaurantAgent as RA


if __name__ == "__main__":
    concierge = RA()
    
    concierge.ask("Find me a good spot for Asian food around the Ntinda or Nakawa neighborhood.")
