import pytest
from unittest.mock import patch, MagicMock
import requests

from app.exceptions import UnprocessableEntityError


@patch("app.external.nominatim_api.requests.get")
def test_get_location_success(mock_get, nominatim_service):
    mock_response = MagicMock()
    mock_response.json.return_value = [{"lat": "10.0", "lon": "20.0"}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    lat, lon = nominatim_service.get_location("Av Paulista")

    assert lat == 10.0
    assert lon == 20.0
    mock_get.assert_called_once()


@patch("app.external.nominatim_api.requests.get")
def test_get_location_request_exception(mock_get, nominatim_service):
    mock_get.side_effect = requests.RequestException("Timeout")

    with pytest.raises(ValueError) as exc:
        nominatim_service.get_location("Av Paulista")

    assert "Failed to fetch location" in str(exc.value)


@patch("app.external.nominatim_api.requests.get")
def test_get_location_not_found(mock_get, nominatim_service):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with pytest.raises(UnprocessableEntityError):
        nominatim_service.get_location("Invalid Place")
