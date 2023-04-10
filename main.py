#!/usr/bin/python3

import os
import math
import time
from datetime import datetime

from config import CONFIG, wakeup_time_s
from draw_weather import draw_everything, draw_error
from inkyWeatherFun.boxes import get_owslot_dict
# from lib.waveshare_epd import epd2in13b_V4
# epd = epd2in13b_V4.EPD()

from openweather import get_current, get_forecast5

while True:
    # Every 30min we reload
    # if (math.floor(time.time() / 60) % CONFIG['update_freq_min']) == 0:
    print("drawing")
    try:
        weather = get_current(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
        fcast = get_forecast5(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
        # raise Exception("msg lol")
    except Exception as e:
        draw_error(e)
    else:
        draw_everything(weather, fcast)
    print("sleeping")
    time.sleep(wakeup_time_s)
