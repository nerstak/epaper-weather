import time

import board
import adafruit_dht

from config import log, CONFIG
from metrics_handler import log_local_temperature_humidity

# Replace D4 with whatever pin data actually is connected
_pin = board.D4

def _create_connection_sensor() -> adafruit_dht.DHT22:
    """
    Connect to sensor
    :return: Object of DHT22 with connection initialized
    """
    return adafruit_dht.DHT22(_pin)

def exit_dht_sensor(dhtDevice: adafruit_dht.DHT22):
    """
    Properly exit sensor
    """
    dhtDevice.exit()

def get_temperature_humidity() -> (float, float):
    """
    Get temperature & humidity
    :return: (temperature, humidity)
    """
    temp, hum =  retrieve_data_sensor()
    if CONFIG["metrics"]["record_metrics"]:
       log_local_temperature_humidity(temp, hum)
    return temp, hum


def retrieve_data_sensor(tries = 5) -> (float, float):
    """
    Retrieve data from sensor
    :param tries: number of time to accept an error
    :return: (temperature, humidity)
    """
    dhtDevice = _create_connection_sensor()
    nb_try = 0
    while nb_try < tries:
        time.sleep(1)
        try:
            temp = float(dhtDevice.temperature)
            hum = float(dhtDevice.humidity)

            # Sometimes, the sensor will return 25.5, which is incorrect
            # See https://forum.arduino.cc/t/arduino-due-dht22-wrong-value/1035449/3
            if temp == 25.5 and hum == 25.5:
                raise RuntimeError("Wrong value: 25.5")
        except RuntimeError as error:
            log.warn(error)
            nb_try+=1
        except Exception as error:
            dhtDevice.exit()
            raise error
        else:
            dhtDevice.exit()
            return temp, hum
    dhtDevice.exit()
