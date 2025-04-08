import http
from unittest.mock import MagicMock
from app.exceptions import ConflictError, NotFoundError


BASE_URL = "/api/v1/locations/"


def make_location_response(id="123", name="Av. Paulista"):
    return {"id": id, "name": name, "lat": 10.0, "lon": 20.0}


def test_create_location_success(client, mock_service):
    mock_service.create_location.return_value.model_dump.return_value = make_location_response()

    response = client.post(BASE_URL, json={"name": "Av. Paulista"})

    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["name"] == "Av. Paulista"
    mock_service.create_location.assert_called_once_with("Av. Paulista")


def test_create_location_conflict(client, mock_service):
    mock_service.create_location.side_effect = ConflictError()

    response = client.post(BASE_URL, json={"name": "Duplicate Name"})

    assert response.status_code == http.HTTPStatus.CONFLICT
    assert "error" in response.json


def test_get_location_by_id_success(client, mock_service):
    mock_service.get_location_by_id.return_value.model_dump.return_value = make_location_response()

    response = client.get(f"{BASE_URL}123")

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["id"] == "123"


def test_get_location_by_id_not_found(client, mock_service):
    mock_service.get_location_by_id.side_effect = NotFoundError()

    response = client.get(f"{BASE_URL}999")

    assert response.status_code == http.HTTPStatus.NOT_FOUND
    assert "error" in response.json


def test_update_location_success(client, mock_service):
    mock_service.update_location.return_value.model_dump.return_value = make_location_response(name="Updated Name")

    response = client.put(f"{BASE_URL}123", json={"name": "Updated Name"})

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["name"] == "Updated Name"


def test_update_location_conflict(client, mock_service):
    mock_service.update_location.side_effect = ConflictError()

    response = client.put(f"{BASE_URL}123", json={"name": "Duplicate Name"})

    assert response.status_code == http.HTTPStatus.CONFLICT
    assert "error" in response.json


def test_delete_location_success(client, mock_service):
    mock_service.delete_location.return_value = True

    response = client.delete(f"{BASE_URL}123")

    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_location_not_found(client, mock_service):
    mock_service.delete_location.side_effect = NotFoundError()

    response = client.delete(f"{BASE_URL}999")

    assert response.status_code == http.HTTPStatus.NOT_FOUND
    assert "error" in response.json


def test_get_nearby_locations_success(client, mock_service):
    mock_service.get_nearby_locations.return_value = [
        MagicMock(model_dump=MagicMock(return_value={
            "id": "1", "name": "Place A", "lat": 10.0, "lon": 20.0, "distance_km": 1.2
        })),
        MagicMock(model_dump=MagicMock(return_value={
            "id": "2", "name": "Place B", "lat": 10.1, "lon": 20.1, "distance_km": 3.4
        })),
    ]

    response = client.get(f"{BASE_URL}nearby?lat=10.0&lon=20.0&radius_km=5.0")

    assert response.status_code == http.HTTPStatus.OK
    assert isinstance(response.json, list)
    assert len(response.json) == 2
