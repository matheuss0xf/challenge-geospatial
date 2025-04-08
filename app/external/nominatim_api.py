from functools import lru_cache

import requests

from app.exceptions import UnprocessableEntityError
from app.logger import logger


class NominatimAPI:
    def __init__(self, config):
        self.config = config

    @lru_cache(maxsize=100)
    def get_location(self, location_name: str) -> tuple[float, float]:
        try:
            response = requests.get(
                self.config.NOMINATIM_API,
                params={'q': location_name, 'format': 'json', 'limit': 1},
                headers={'User-Agent': 'location-api'},
                timeout=30,
            )
            response.raise_for_status()
            results = response.json()
            if not results:
                logger.error(f'No results found for location: {location_name}')
                raise UnprocessableEntityError()
            return float(results[0]['lat']), float(results[0]['lon'])
        except requests.RequestException as e:
            logger.error(f'Request to Nominatim API failed: {e}')
            raise ValueError('Failed to fetch location')
