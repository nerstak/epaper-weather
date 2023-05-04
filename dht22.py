import board
import adafruit_dht

from config import log, CONFIG
from metrics_handler import log_local_temperature_humidity

# Replace D4 with whatever pin data actually is connected
_pin = board.D4

def _create_connection_sensor() -> adafruit_dht.DHT22:
    return adafruit_dht.DHT22(_pin)

dhtDevice = _create_connection_sensor()

def exit_dht_sensor():
    dhtDevice.exit()

def get_temperature_humidity() -> (float, float):
    temp, hum =  retrieve_data_sensor()
    if CONFIG["metrics"]["record_metrics"]:
       log_local_temperature_humidity(temp, hum)
    return temp, hum


def retrieve_data_sensor(tries = 5) -> (float, float):
    try:
        temp = float(dhtDevice.temperature)
        hum = float(dhtDevice.humidity)
    except RuntimeError as error:
        log.warn(error)
    except Exception as error:
        dhtDevice.exit()
        raise error
    else:
        return temp, hum
