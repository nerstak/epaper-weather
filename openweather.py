from functools import lru_cache

import requests

from config import CONFIG

_URL_FORECAST5 = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units={}"
_URL_CURRENT_WEATHER = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units={}"

# Because we don't want to call too many times the API, we cache responses
# The way it works is that basically each period has an id (nb 0, nb 1, etc.) from timestamp
# As long as the id does not change, we don't need to re-execute API calls

@lru_cache()
def get_current(lat: float, lon: float, unit: str, ttl_hash) -> dict:
    uri = _URL_CURRENT_WEATHER.format(lat, lon, CONFIG["API_KEY"], unit)
    return _get_weather(uri)


@lru_cache()
def get_forecast5(lat: float, lon: float, unit: str, ttl_hash) -> dict:
    uri = _URL_FORECAST5.format(lat, lon, CONFIG["API_KEY"], unit)
    return _get_weather(uri)


def _get_weather(uri: str) -> dict:
    """
    Get weather from preformatted uri
    :param uri: URI
    :return: dict or error
    """
    resp = requests.get(uri)
    result = resp.json()

    if 200 > int(result['cod']) >= 300:
        raise Exception("{}: {}".format(result['cod'], result['message']))

    return result
