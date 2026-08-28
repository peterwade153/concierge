from typing import Dict, List, Any
import logging

from agent.utils.nominatim import get_location_coordinates
from agent.utils.foursquare import search_foursquare_restaurants, extract_cuisines


logger = logging.getLogger(__name__)

def search_restaurants_by_area(area: str) -> List[Dict[str, Any]]:
    """
    Searches for highly-rated local restaurants within a specific neighborhood or division.
    
    Args:
        area: The neighborhood or district to filter by (e.g., 'Nakawa', 'Naguru', 'Ntinda').
    """

    area_coords = get_location_coordinates(area)

    if not area_coords:
        logger.warning("Could not resolve coordinates.")
        return []
    lat, lon = area_coords
    restaurants = search_foursquare_restaurants(lat, lon)
    return restaurants

def filter_by_cuisine(restaurants: List[Dict[str, Any]], cuisine: str) -> List[Dict[str, Any]]:
    """
    Filters a list of restaurants to only include those serving a specific type of food.
    
    Args:
        restaurants: A list of restaurant dictionaries.
        cuisine: The type of food desired (e.g., 'Korean', 'Pizza', 'Middle Eastern').
    """
    cuisines = extract_cuisines(restaurants)
    filtered = [r for r in restaurants if cuisine in cuisines]
    return filtered


AVAILABLE_TOOLS = {
    "search_restaurants_by_area": search_restaurants_by_area,
    "filter_by_cuisine": filter_by_cuisine
}

TOOL_SCHEMAS = {
    "search_restaurants_by_area": {
        "type": "function",
        "function": {
            "name": "search_restaurants_by_area",
            "description": "Searches for highly-rated local restaurants within a specific neighborhood or division.",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {
                        "type": "string",
                        "description": "The neighborhood or district to filter by (e.g., 'Nakawa', 'Naguru', 'Ntinda').",
                    }
                },
                "required": ["area"],
            },
        },
    },
    "filter_by_cuisine": {
        "type": "function",
        "function": {
            "name": "filter_by_cuisine",
            "description": "Filters a list of restaurants to only include those serving a specific type of food.",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurants": {
                        "type": "array",
                        "description": "A list of restaurant dictionaries to filter.",
                        "items": {"type": "object"},
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "The type of food desired (e.g., 'Korean', 'Pizza', 'Middle Eastern').",
                    },
                },
                "required": ["restaurants", "cuisine"],
            },
        },
    },
}
