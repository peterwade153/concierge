from typing import Dict, List, Any


RESTAURANT_DB = [
    {
        "name": "Olives Restaurant & Bar",
        "location": "Naguru Dr, Nakawa",
        "cuisine": "Continental, Pizza & Cocktails",
        "price_range": "UGX 40,000 - 100,000",
        "rating": 4.3,
        "specialty": "Modern fusion, premium wood-fired pizzas, and outdoor ambiance."
    },
    {
        "name": "Yums Cafe",
        "location": "Kiwatule Rd, Ntinda",
        "cuisine": "Italian, Barbecue & Local Fusion",
        "price_range": "UGX 40,000 - 60,000",
        "rating": 4.5,
        "specialty": "Chicken tikka masala and photogenic floral decor vibes."
    },
    {
        "name": "La Casita Restaurant & Bar",
        "location": "Ntinda II Rd, Nakawa",
        "cuisine": "Korean & Japanese",
        "price_range": "UGX 40,000 - 120,000",
        "rating": 4.3,
        "specialty": "Authentic Bulgogi, Kimbap, and scenic hilltop breeze views."
    },
    {
        "name": "Middle East Restaurant",
        "location": "Kira Rd, Naguru",
        "cuisine": "Middle Eastern",
        "price_range": "UGX 40,000 - 120,000",
        "rating": 4.3,
        "specialty": "Chicken shawarma, falafel, hummus, and 24-hour service."
    }
]


def search_restaurants_by_area(area: str) -> List[Dict[str, Any]]:
    """
    Searches for highly-rated local restaurants within a specific neighborhood or division.
    
    Args:
        area: The neighborhood or district to filter by (e.g., 'Nakawa', 'Naguru', 'Ntinda').
    """
    results = [r for r in RESTAURANT_DB if area.lower() in r["location"].lower()]
    return results if results else [{"message": f"No listed venues found specifically matching '{area}'."}]


def filter_by_cuisine(restaurants: List[Dict[str, Any]], cuisine: str) -> List[Dict[str, Any]]:
    """
    Filters a list of restaurants to only include those serving a specific type of food.
    
    Args:
        restaurants: A list of restaurant dictionaries.
        cuisine: The type of food desired (e.g., 'Korean', 'Pizza', 'Middle Eastern').
    """
    # Simple check to see if the cuisine keyword exists in the restaurant entry
    filtered = [r for r in restaurants if "cuisine" in r and cuisine.lower() in r["cuisine"].lower()]
    return filtered if filtered else [{"message": f"No options matching the cuisine '{cuisine}' in this subset."}]


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
