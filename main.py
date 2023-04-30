#!/usr/bin/python3

import math
import time
from datetime import datetime
import logging
import atexit

from config import CONFIG, wakeup_time_s
from draw_weather import draw_everything, draw_error, clear_screen

from openweather import get_current, get_forecast5

atexit.register(clear_screen)
error_count = 0
starting = True
while True:
    current_time = time.time()

    logging.debug("New loop iteration")
    # We reload if we waited long enough or if there was an error the previous time
    if (math.floor(current_time / 60) % CONFIG['update_freq_min']) == 0 or error_count > 0 or starting:
        starting = False
        # Clearing screen at 3AM
        if datetime.now().strftime('%H') == '03':
            clear_screen()

        try:
            weather = get_current(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
            fcast = get_forecast5(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
        except Exception as e:
            logging.error(e)
            error_count += 1
            draw_error(e)
        else:
            logging.debug("Drawing image")
            draw_everything(weather, fcast)
            error_count = 0
    # TODO: Wait more if error count is high
    time.sleep(wakeup_time_s)
