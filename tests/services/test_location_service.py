import pytest
from app.schemas.location_schema import LocationOut, LocationNearbyOut
from app.exceptions import ConflictError, NotFoundError, UnprocessableEntityError


def test_create_location_success(service, mock_repo, mock_nominatim):
    mock_repo.get_location_by_name.return_value = None
    mock_nominatim.get_location.return_value = (10.0, 20.0)
    mock_repo.create_location.return_value = {"id": "123", "name": "Av. Paulista", "lat": 10.0, "lon": 20.0}

    result = service.create_location("Av. Paulista")

    assert isinstance(result, LocationOut)
    assert result.name == "Av. Paulista"
    mock_repo.get_location_by_name.assert_called_once_with("Av. Paulista")


def test_create_location_conflict(service, mock_repo):
    mock_repo.get_location_by_name.return_value = {"id": "123"}

    with pytest.raises(ConflictError, match="Location already exists"):
        service.create_location("Av. Paulista")


def test_create_location_unprocessable(service, mock_repo, mock_nominatim):
    mock_repo.get_location_by_name.return_value = None
    mock_nominatim.get_location.return_value = (None, None)

    with pytest.raises(UnprocessableEntityError, match="Name not found"):
        service.create_location("Nonexistent Place")


def test_get_location_by_id_success(service, mock_repo):
    mock_repo.get_location_by_id.return_value = {
        "id": "123", "name": "Av. Paulista", "lat": 10.0, "lon": 20.0
    }

    result = service.get_location_by_id("123")

    assert isinstance(result, LocationOut)
    assert result.id == "123"


def test_get_location_by_id_not_found(service, mock_repo):
    mock_repo.get_location_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.get_location_by_id("999")


def test_get_nearby_locations(service, mock_repo):
    mock_repo.get_nearby_locations.return_value = [
        {"id": "1234", "name": "Test A", "lat": 10.0, "lon": 20.0, "distance_km": 1.2},
        {"id": "12345", "name": "Test B", "lat": 10.1, "lon": 20.1, "distance_km": 3.5}
    ]

    result = service.get_nearby_locations(10.0, 20.0, 5.0)

    assert isinstance(result, list)
    assert isinstance(result[0], LocationNearbyOut)
    assert len(result) == 2


def test_update_location_success(service, mock_repo, mock_nominatim):
    mock_repo.get_location_by_id.return_value = {"id": "123", "name": "Old", "lat": 1.0, "lon": 1.0}
    mock_repo.get_location_by_name.return_value = None
    mock_nominatim.get_location.return_value = (10.0, 20.0)
    mock_repo.update_location.return_value = {"id": "123", "name": "New", "lat": 10.0, "lon": 20.0}

    result = service.update_location("123", "New")

    assert isinstance(result, LocationOut)
    assert result.name == "New"


def test_update_location_not_found(service, mock_repo):
    mock_repo.get_location_by_id.return_value = None

    with pytest.raises(NotFoundError, match="Location not found exists"):
        service.update_location("999", "New")


def test_update_location_conflict(service, mock_repo):
    mock_repo.get_location_by_id.return_value = {"id": "123", "name": "Old"}
    mock_repo.get_location_by_name.return_value = {"id": "999"}

    with pytest.raises(ConflictError, match="Location already exists"):
        service.update_location("123", "Existing Name")


def test_update_location_unprocessable(service, mock_repo, mock_nominatim):
    mock_repo.get_location_by_id.return_value = {"id": "123", "name": "Old"}
    mock_repo.get_location_by_name.return_value = None
    mock_nominatim.get_location.return_value = (None, None)

    with pytest.raises(UnprocessableEntityError, match="Name not found"):
        service.update_location("123", "Invalid Name")


def test_delete_location_success(service, mock_repo):
    mock_repo.get_location_by_id.return_value = {"id": "123"}
    mock_repo.delete_location.return_value = True

    result = service.delete_location("123")
    assert result is True


def test_delete_location_not_found(service, mock_repo):
    mock_repo.get_location_by_id.return_value = None

    with pytest.raises(NotFoundError, match="Location not found"):
        service.delete_location("999")
