import pytest
from unittest.mock import patch, MagicMock, Mock

from app.external.nominatim_api import NominatimAPI
from main import create_app
from app.repositories.location_repository import LocationRepository
from app.services.location_service import LocationService


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_service():
    mock = MagicMock()
    with patch("app.controllers.location.Registry") as mock_registry:
        mock_registry.return_value.location.return_value = mock
        yield mock


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def mock_nominatim():
    return Mock()

@pytest.fixture
def nominatim_config():
    mock = MagicMock()
    mock.NOMINATIM_API = "https://nominatim.openstreetmap.org/search"
    return mock

@pytest.fixture
def nominatim_service(nominatim_config):
    return NominatimAPI(nominatim_config)

@pytest.fixture
def config():
    return Mock()


@pytest.fixture
def service(mock_repo, mock_nominatim, config):
    return LocationService(mock_repo, mock_nominatim, config)

@pytest.fixture
def mock_db():
    conn = MagicMock()
    cur = MagicMock()
    db = MagicMock()
    db.get_cursor.return_value.__enter__.return_value = (conn, cur)
    return db, cur


@pytest.fixture
def repository(mock_db):
    config = MagicMock()
    db, _ = mock_db
    return LocationRepository(config, db)