import requests
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def get_location_coordinates(place_name: str) -> Optional[Tuple[float, float]]:
    """Step 1: Geocode place string using Nominatim with logging."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "concierge-agent/1.0 (concierge-agent@gmail.com)"}
    
    logger.info(f"Geocoding '{place_name}' via Nominatim...")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            logger.warning(f"Nominatim returned no results for '{place_name}'.")
            return None
            
        lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
        logger.info(f"Successfully resolved '{place_name}' to ({lat}, {lon})")
        print('-------------------------')
        print(f"Successfully resolved '{place_name}' to ({lat}, {lon})")
        return lat, lon
        
    except requests.exceptions.Timeout:
        logger.error(f"Geocoding request timed out for '{place_name}'.")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Nominatim API HTTP Error: {http_err} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network error during geocoding: {req_err}")
    except Exception as e:
        logger.error(f"Unexpected error resolving coordinates: {e}")
        
    return None
