from .config import Config
from .database.sqlite import DatabaseSqlite
from .external.nominatim_api import NominatimAPI
from .repositories.location_repository import LocationRepository
from .services.location_service import LocationService


class Registry:
    def __init__(self):
        self.config = Config()

    def location(self) -> LocationService:
        return LocationService(
            LocationRepository(self.config, DatabaseSqlite(self.config)),
            NominatimAPI(self.config),
            self.config,
        )
