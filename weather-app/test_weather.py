import pytest
from unittest.mock import patch, MagicMock

from weather_app import (
    convert_fahrenheit_to_celsius,
    convert_celsius_to_fahrenheit,
    get_weather_data,
)


class TestConvertFahrenheitToCelsius:
    def test_freezing_point(self):
        assert convert_fahrenheit_to_celsius(32) == 0

    def test_boiling_point(self):
        assert convert_fahrenheit_to_celsius(212) == 100

    def test_body_temperature(self):
        assert convert_fahrenheit_to_celsius(98.6) == pytest.approx(37.0, rel=1e-3)

    def test_negative_fahrenheit(self):
        assert convert_fahrenheit_to_celsius(-40) == -40


class TestConvertCelsiusToFahrenheit:
    def test_freezing_point(self):
        assert convert_celsius_to_fahrenheit(0) == 32

    def test_boiling_point(self):
        assert convert_celsius_to_fahrenheit(100) == 212

    def test_body_temperature(self):
        assert convert_celsius_to_fahrenheit(37) == pytest.approx(98.6, rel=1e-3)

    def test_negative_celsius(self):
        assert convert_celsius_to_fahrenheit(-40) == -40


class TestGetWeatherData:
    SAMPLE_RESPONSE = {
        "name": "London",
        "sys": {"country": "GB"},
        "weather": [{"description": "clear sky"}],
        "main": {
            "temp": 15.0,
            "feels_like": 14.0,
            "temp_min": 12.0,
            "temp_max": 18.0,
            "humidity": 72,
        },
    }

    @patch("weather_app.requests.get")
    def test_successful_request_returns_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.SAMPLE_RESPONSE
        mock_get.return_value = mock_response

        result = get_weather_data("London")

        assert result == self.SAMPLE_RESPONSE

    @patch("weather_app.requests.get")
    def test_request_uses_correct_url_and_city(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.SAMPLE_RESPONSE
        mock_get.return_value = mock_response

        get_weather_data("Paris")

        call_args = mock_get.call_args
        assert call_args[0][0] == "https://api.openweathermap.org/data/2.5/weather"
        assert call_args[1]["params"]["q"] == "Paris"
        assert call_args[1]["params"]["units"] == "metric"

    @patch("weather_app.requests.get")
    def test_404_raises_runtime_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(RuntimeError, match="404"):
            get_weather_data("UnknownCity")

    @patch("weather_app.requests.get")
    def test_500_raises_runtime_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with pytest.raises(RuntimeError, match="500"):
            get_weather_data("London")

    @patch("weather_app.requests.get")
    def test_201_status_is_accepted(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = self.SAMPLE_RESPONSE
        mock_get.return_value = mock_response

        result = get_weather_data("London")
        assert result == self.SAMPLE_RESPONSE
