from typing import List, Optional

from app.exceptions import ConflictError, NotFoundError, UnprocessableEntityError
from app.logger import logger
from app.schemas.location_schema import LocationIn, LocationNearbyOut, LocationOut


class LocationService:
    def __init__(self, location_repository, nominatim_api, config) -> None:
        self.repo = location_repository
        self.nominatim_api = nominatim_api
        self.config = config

    def create_location(self, name: LocationIn):
        name_exists = self.repo.get_location_by_name(name)
        if name_exists:
            logger.error(f'Location with name {name} already exists')
            raise ConflictError('Location already exists')

        lat, lon = self.nominatim_api.get_location(name)
        if not lat or not lon:
            logger.error(f'Failed to get coordinates for location: {name}')
            raise UnprocessableEntityError('Name not found')
        location = self.repo.create_location(name, lat, lon)
        return LocationOut(**location)

    def get_location_by_id(self, location_id: str) -> LocationOut:
        location = self.repo.get_location_by_id(location_id)
        if not location:
            logger.error(f'Location with ID {location_id} not found')
            raise NotFoundError()
        return LocationOut(**location)

    def get_nearby_locations(self, lat: float, lon: float, radius_km: float) -> List[LocationNearbyOut]:
        locations = self.repo.get_nearby_locations(lat, lon, radius_km)
        return [LocationNearbyOut(**loc) for loc in locations]

    def update_location(self, location_id: str, name: str) -> Optional[LocationOut]:
        location_exists = self.repo.get_location_by_id(location_id)
        if not location_exists:
            logger.error(f'Location with name {name} or id {location_id} not found')
            raise NotFoundError('Location not found exists')

        name_exists = self.repo.get_location_by_name(name)
        if name_exists and name_exists.get('id') != location_id:
            logger.error(f'Location with name {name} already exists')
            raise ConflictError('Location already exists')

        lat, lon = self.nominatim_api.get_location(name)
        if not lat or not lon:
            logger.error(f'Failed to get coordinates for location: {name}')
            raise UnprocessableEntityError('Name not found')
        location = self.repo.update_location(location_id, name, lat, lon)
        return LocationOut(**location)

    def delete_location(self, location_id: str) -> bool:
        location_exists = self.repo.get_location_by_id(location_id)
        if not location_exists:
            logger.error(f'Location with ID {location_id} not found')
            raise NotFoundError('Location not found')
        return self.repo.delete_location(location_id)
