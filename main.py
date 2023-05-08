#!/usr/bin/python3

import math
import time
from datetime import datetime
import atexit

from config import CONFIG, wakeup_time_s, log
from dht22 import get_temperature_humidity
from draw_weather import draw_image, draw_error
from epd_handler import clear_screen

from openweather import get_current, get_forecast5
from utils import get_ttl_hash

atexit.register(clear_screen)

error_count = 0
starting = True
while True:
    ttl_hash = get_ttl_hash(CONFIG['refresh_period_min']['data'] * 60)

    log.debug("New loop iteration")
    # We reload if we waited long enough or if there was an error the previous time
    if (math.floor(time.time() / 60) % CONFIG['refresh_period_min']['screen']) == 0 or error_count > 0 or starting:
        starting = False
        # Clearing screen at 3AM
        if datetime.now().strftime('%H') == '03':
            clear_screen()

        try:
            weather = get_current(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'], ttl_hash)
            fcast = get_forecast5(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'], ttl_hash)
            local_data = get_temperature_humidity()
        except Exception as e:
            log.error(e)
            error_count += 1
            draw_error(e, str(wakeup_time_s))
        else:
            log.debug("Drawing image")
            draw_image(weather, fcast, local_data)
            error_count = 0

    # TODO: Wait more if error count is high
    time.sleep(wakeup_time_s - math.ceil(time.time() % wakeup_time_s) + 1)
