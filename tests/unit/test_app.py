import pytest
from app import fetch_weather_data

def test_fetch_weather_data():
    weather_data = fetch_weather_data()
    assert isinstance(weather_data, list)
    if weather_data:
        assert 'Created' in weather_data[0]
        assert 'Datum' in weather_data[0]
        assert 'Hour' in weather_data[0]
        assert 'Precipitation' in weather_data[0]
        assert 'Provider' in weather_data[0]

def test_fetch_weather_data_empty():
    weather_data = []
    assert weather_data == []