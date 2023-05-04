import requests

from config import CONFIG, log

_URL_INFLUX = "http://{}/write?db={}"
_URL_INFLUX_FORMATTED = _URL_INFLUX.format(
    CONFIG["metrics"].get("database_url", ""),
    CONFIG["metrics"].get("database_name", ""),
)


def format_to_influx(metric_name: str, value: float, tags: dict[str, str]):
    """
    Format data to InfluxDB
    :param metric_name: Metric name
    :param value: Value of measurement
    :param tags: List of tags
    :return: Well formatted metric
    """
    str_tags = ','.join('='.join([k, v]) for k, v in tags.items())
    return ' '.join([
        ','.join([metric_name, str_tags]),
        'value=' + str(value)
    ])


def log_current_weather(weather: dict):
    """
    Save current weather data
    :param weather: data from OWM
    """
    tags = {
        "city": CONFIG['city']
    }
    weather_temp = format_to_influx("owm.weather.temperature", weather["main"]["temp"], tags)
    weather_feels_temp = format_to_influx("owm.weather.feels_temperature", weather["main"]["feels_like"], tags)
    weather_humidity = format_to_influx("owm.weather.humidity", weather["main"]["humidity"], tags)
    weather_wind = format_to_influx("owm.weather.wind_speed", weather["wind"]["speed"], tags)
    weather_cloudiness = format_to_influx("owm.weather.cloudiness", weather["clouds"]["all"], tags)

    _post_metrics([
        weather_temp,
        weather_feels_temp,
        weather_humidity,
        weather_wind,
        weather_cloudiness,
    ])

def log_local_temperature_humidity(temperature: float, humidity: float):
    """
    Save local temperature & humidity
    :param temperature: Local temperature
    :param humidity: Local humidity
    """
    tags = {
        "city": CONFIG['city']
    }
    weather_temp = format_to_influx("local.temperature", temperature, tags)
    weather_humidity = format_to_influx("local.humidity", humidity, tags)

    _post_metrics([
        weather_temp,
        weather_humidity,
    ])

def _post_metrics(metrics: [str]):
    """
    Post metrics on a InfluxDb
    :param metrics: Array of metrics
    """
    res = requests.post(_URL_INFLUX_FORMATTED, '\n'.join(metrics))
    if res.status_code >= 300:
        log.error(res.text)
