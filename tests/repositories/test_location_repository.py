import pytest

def test_create_location(repository, mock_db):
    _, cur = mock_db
    result = repository.create_location("Test Av. Paulista", 10.0, 20.0)

    cur.execute.assert_called_once()
    assert result["name"] == "Test Av. Paulista"
    assert result["lat"] == 10.0
    assert result["lon"] == 20.0
    assert "id" in result


def test_get_location_by_id_found(repository, mock_db):
    _, cur = mock_db
    cur.fetchone.return_value = {"id": "1", "name": "Av. Paulista", "lat": 10.0, "lon": 20.0}

    result = repository.get_location_by_id("1")

    cur.execute.assert_called_once()
    assert result["id"] == "1"


def test_get_location_by_id_not_found(repository, mock_db):
    _, cur = mock_db
    cur.fetchone.return_value = None

    result = repository.get_location_by_id("not found")
    assert result is None


def test_get_location_by_name_found(repository, mock_db):
    _, cur = mock_db
    cur.fetchone.return_value = {"id": "1", "name": "Av. Paulista", "lat": 10.0, "lon": 20.0}

    result = repository.get_location_by_name("Av. Paulista")

    cur.execute.assert_called_once()
    assert result["name"] == "Av. Paulista"

def test_get_location_by_name_not_found(repository, mock_db):
    _, cur = mock_db
    cur.fetchone.return_value = None

    result = repository.get_location_by_name("not found")
    assert result is None

def test_get_nearby_locations(repository, mock_db):
    _, cur = mock_db
    cur.fetchall.return_value = [
        {"id": "1", "name": "Test A", "lat": 10.0, "lon": 20.0, "distance_km": 1.0},
        {"id": "2", "name": "Test B", "lat": 10.1, "lon": 20.1, "distance_km": 3.0},
    ]

    result = repository.get_nearby_locations(10.0, 20.0, 5.0)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Test A"


def test_update_location_success(repository, mock_db):
    _, cur = mock_db
    cur.rowcount = 1

    result = repository.update_location("123", "Updated", 11.0, 22.0)

    assert result["id"] == "123"
    assert result["name"] == "Updated"


def test_update_location_not_found(repository, mock_db):
    _, cur = mock_db
    cur.rowcount = 0

    result = repository.update_location("999", "Not Found", 0.0, 0.0)
    assert result is None


def test_delete_location_success(repository, mock_db):
    _, cur = mock_db
    cur.rowcount = 1

    result = repository.delete_location("123")
    assert result is True


def test_delete_location_not_found(repository, mock_db):
    _, cur = mock_db
    cur.rowcount = 0

    result = repository.delete_location("not found")
    assert result is False
