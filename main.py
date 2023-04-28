#!/usr/bin/python3

import math
import time
from datetime import datetime

from config import CONFIG, wakeup_time_s
from draw_weather import draw_everything, draw_error, clear_screen

from openweather import get_current, get_forecast5

while True:
    error_count = 0
    current_time = time.time()

    # We reload if we waited long enough or if there was an error the previous time
    if (math.floor(current_time / 60) % CONFIG['update_freq_min']) == 0 or error_count > 0 or True:
        # Clearing screen at 3AM
        if datetime.now().strftime('%H') == '03':
            clear_screen()

        try:
            weather = get_current(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
            fcast = get_forecast5(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
        except Exception as e:
            error_count += 1
            draw_error(e)
        else:
            draw_everything(weather, fcast)
            error_count = 0
    time.sleep(wakeup_time_s)
