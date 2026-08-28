import requests
import logging
import os
from typing import List, Dict

logger = logging.getLogger(__name__)


def search_foursquare_restaurants(lat: float, lon: float, radius: int = 8000) -> List[Dict]:
    """Fetch nearby restaurants using Foursquare Places API with logging."""

    if not os.environ.get("FOURSQUARE_API_KEY"):
        raise ValueError("FOURSQUARE_API_KEY environment variable is not set.")

    url = "https://places-api.foursquare.com/places/search"
    params = {
        "ll": f"{lat},{lon}",
        "radius": radius, # 5km
        "categories": "13000",  # Dining & Drinking
        "limit": 20
    }
    headers = {
        "X-Places-Api-Version": "2025-06-17",
        "Accept": "application/json",
        "Authorization": os.environ.get("FOURSQUARE_API_KEY")
    }
    
    logger.info(f"Querying Foursquare for restaurants near ({lat}, {lon}) within {radius}m...")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 429:
            logger.error("Foursquare API rate limit exceeded.")
            return []
            
        response.raise_for_status()
        
        results = response.json().get("results", [])
        if not results:
            logger.info("Foursquare returned 0 restaurants for this location.")
        else:
            logger.info(f"Found {len(results)} restaurants via Foursquare.")
            
        return results
        
    except requests.exceptions.Timeout:
        logger.error("Foursquare API request timed out.")
    except requests.exceptions.HTTPError as http_err:
        try:
            error_details = response.json()
            logger.error(f"Foursquare HTTP Error: {http_err}. Details: {error_details}")
        except ValueError:
            logger.error(f"Foursquare HTTP Error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network error communicating with Foursquare: {req_err}")
    except Exception as e:
        logger.error(f"Unexpected error querying Foursquare: {e}")
        
    return []


def extract_cuisines(place_data: dict) -> list[str]:
    """Extract cuisine names from a Foursquare place object.
    Sample response
    : {
        "results": [
            {
            "fsq_id": "4b058810f964a52033b022e3",
            "name": "Rubirosa Pizza & Ristorante",
            "categories": [
                {
                "id": 13065,
                "name": "Italian Restaurant"
                },
                {
                "id": 13064,
                "name": "Pizzeria"
                }
            ],
            "price": 2,
            "rating": 8.9,
            "popularity": 0.9852,
            "website": "https://www.rubirosanyc.com",
            "tel": "(212) 965-0500",
            "hours": {
                "display": "Mon-Sun 11:30 AM-11:00 PM",
                "is_local_holiday": false,
                "open_now": true,
                "regular": [
                {
                    "close": "2300",
                    "day": 1,
                    "open": "1130"
                }
                ]
            },
            "features": {
                "payment": {
                "credit_cards": {
                    "accepts_credit_cards": true
                }
                },
                "food_and_drink": {
                "alcohol": {
                    "full_bar": true
                },
                "reservations": true
                },
                "services": {
                "delivery": true,
                "takeout": true
                }
            },
            "photos": [
                {
                "id": "5fa23bc01e23a418579d40a2",
                "created_at": "2020-11-04T05:22:40.000Z",
                "prefix": "https://fastly.4sqi.net/img/general/",
                "suffix": "/5891234_ABCxyz123.jpg",
                "width": 1920,
                "height": 1440
                }
            ]
            }
        ]
    }
    """
    cuisines = []
    
    for category in place_data.get("categories", []):
        cat_name = category.get("name", "")
        if "Restaurant" in cat_name and cat_name != "Restaurant":
            clean_cuisine = cat_name.replace(" Restaurant", "").strip().lower()
            cuisines.append(clean_cuisine)
        else:
            cuisines.append(cat_name.lower())
    return cuisines
