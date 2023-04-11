#!/usr/bin/python3

import os
import math
import time
from datetime import datetime

from config import CONFIG, wakeup_time_s
from draw_weather import draw_everything, draw_error
# from lib.waveshare_epd import epd2in13b_V4
# epd = epd2in13b_V4.EPD()

from openweather import get_current, get_forecast5

while True:
    error_count = 0
    # We reload if we waited long enough or if there was an error the previous time
    if (math.floor(time.time() / 60) % CONFIG['update_freq_min']) == 0 or error_count > 0 or True:
        print("drawing")
        try:
            weather = get_current(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
            fcast = get_forecast5(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
            # raise Exception("msg lol")
        except Exception as e:
            error_count += 1
            draw_error(e)
        else:
            draw_everything(weather, fcast)
            error_count = 0
    print("sleeping")
    time.sleep(wakeup_time_s)
