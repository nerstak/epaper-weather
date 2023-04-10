import requests

from config import CONFIG

URL_FORECAST5 = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units={}"
URL_CURRENT_WEATHER = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units={}"


def get_current(lat: float, lon: float, unit: str) -> dict:
    uri = URL_CURRENT_WEATHER.format(lat, lon, CONFIG["API_KEY"], unit)
    return _get_weather(uri)


def get_forecast5(lat: float, lon: float, unit: str) -> dict:
    uri = URL_FORECAST5.format(lat, lon, CONFIG["API_KEY"], unit)
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


if __name__ == "__main__":
    print(get_forecast5(48.864716, 2.349014, "metric"))
