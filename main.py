#!/usr/bin/python3

import os
import math
from datetime import datetime

from config import CONFIG
from inkyWeatherFun.boxes import get_owslot_dict
# from lib.waveshare_epd import epd2in13b_V4
# epd = epd2in13b_V4.EPD()

from PIL import Image, ImageDraw, ImageFont

from inkyWeatherFun.ttf import ttfUnicode_from_icon, ttfUnicode_from_iconId
from openweather import get_current, get_forecast5

debug = False
full_path = os.path.realpath(__file__)
workdir = os.path.dirname(full_path)

weather = get_current(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])
fcast = get_forecast5(CONFIG['coordinates']['lat'], CONFIG['coordinates']['lon'], CONFIG['units'])

clockFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 28)
dateFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
wCityFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
wIcoFont = ImageFont.truetype(workdir + "/fonts/weathericons-regular-webfont.ttf", 30)
wDetFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
wTempFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 20)
wHumFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 20)
sIcoFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 20)
sTempFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
sHumFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
fBoxFont = ImageFont.truetype(workdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
fBoxWiFont = ImageFont.truetype(workdir + "/fonts/weathericons-regular-webfont.ttf", 20)

wiXmlMap = workdir + "/fonts/values/weathericons.xml"

black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'
grey = 'rgb(235,235,235)'

wx0 = 0
hx0 = 0
wx1 = 250 #epd.width
hx1 = 122 #epd.height

# 180° roatated display
w_wx0 = 0  # current weather area: start width
w_hx0 = 0  # current weather area: start heigth
w_wx1 = wx1  # current weather area: end width
w_hx1 = int(hx1 / 2)  # current weather area: end heigth

f_wx0 = 0  # forecast area: start width
f_hx0 = w_hx1  # forecast area: start heigth
f_wx1 = wx1  # forecast area: end width
f_hx1 = int(hx1 / 2)  # forecast area: end heigth

fBox_rows = 2
fBox_cols = 3
fBox_wx1 = math.floor(w_wx1 / fBox_cols)
fBox_hx1 = math.floor(f_hx1 / fBox_rows)

print("Display width {}, height {}".format(wx1, hx1)) if debug else None
print("forecast box fBox_wx1 {}, fBox_hx1 {}".format(fBox_wx1, fBox_hx1)) if debug else None

img = Image.new("L", (wx1, hx1), 255)
draw = ImageDraw.Draw(img)

# clock 
hours = datetime.now().strftime('%H:%M')
date = datetime.now().strftime('%a, %b %d')

hour_wsize, hour_hsize = draw.textsize(hours, clockFont)
hour_wx0 = 5
hour_hx0 = 0
hour_wx1 = hour_wx0 + hour_wsize
hour_hx1 = hour_hx0 + hour_hsize

date_wsize, date_hsize = draw.textsize(date, dateFont)
date_wx0 = 5  # consider padding?
date_hx0 = hour_hx1
date_wx1 = date_wx0 + date_wsize
date_hx1 = date_hx0 + date_hsize

# draw.rectangle([(hour_wx0, hour_hx0), (hour_wx1, hour_hx1)], fill=iWhite)
draw.text((hour_wx0, hour_hx0), hours, fill=black, font=clockFont)

# draw.rectangle([(date_wx0, date_hx0), (date_wx1, date_hx1)], fill=iWhite)
draw.text((date_wx0, date_hx0), date,  fill=black, font=dateFont)

# current weather
wCity = weather["name"]
wTemp = weather["main"]["temp"]
wHum = weather["main"]["humidity"]
wDet = weather["weather"][0]["description"]
wIcoCode = weather["weather"][0]["icon"]
print("city: {}: temp {}°C, humidity {}%, {} ({})\n\n".format(wCity, wTemp, wHum, wDet, wIcoCode)) if debug else None

wCity_wsize, wCity_hsize = draw.textsize(wCity, wCityFont)
wCity_wx0 = date_wx0  # define padding?
wCity_hx0 = date_hx1
wCity_wx1 = wCity_wx0 + wCity_wsize
wCity_hx1 = wCity_hx0 + wCity_hsize
draw.text((wCity_wx0, wCity_hx0), wCity, fill=black, font=wCityFont)

wIcoUnicode = ttfUnicode_from_icon(wIcoCode, wiXmlMap)
wIco_wsize, wIco_hsize = draw.textsize(wIcoUnicode, wIcoFont)
wIco_wx0 = hour_wx1 + 5  # define padding?
wIco_hx0 = hour_hx0
wIco_wx1 = wIco_wx0 + wIco_wsize
wIco_hx1 = wIco_hx0 + wIco_hsize
draw.text((wIco_wx0, wIco_hx0), wIcoUnicode, fill=black, font=wIcoFont)

wDet_wsize, wDet_hsize = draw.textsize(wDet, wDetFont)
wDet_wx0 = wIco_wx0
wDet_hx0 = wIco_hx1
wDet_wx1 = wIco_wx0 + wDet_wsize
wDet_hx1 = wDet_hx0 + wDet_hsize
draw.text((wDet_wx0, wDet_hx0), wDet,  fill=black, font=wDetFont)

wTemp = str(math.ceil(wTemp)) + "°C"
wTemp_wsize, wTemp_hsize = draw.textsize(wTemp, wTempFont)

wHum = str(wHum) + "%"
wHum_wsize, wHum_hsize = draw.textsize(wHum, wHumFont)

# padding wValCol (temp and hum): half the space left between icon column and right border
wValColPadd_wx0 = max(wIco_wx1, wDet_wx1)
wValColPadd_wsize = int((w_wx1 - wValColPadd_wx0) / 2)

wTempPadd_w = int(((wValColPadd_wsize - wTemp_wsize) / 2))
wTemp_wx0 = wValColPadd_wx0 + wTempPadd_w
wTemp_hx0 = 5  # define padding?
wTemp_wx1 = wTemp_wx0 + wTemp_wsize
wTemp_hx1 = wTemp_hx0 + wTemp_hsize
draw.text((wTemp_wx0, wTemp_hx0), wTemp,  fill=black, font=wTempFont)

wHumPadd_w = int(((wValColPadd_wsize - wHum_wsize) / 2))
wHum_wx0 = wValColPadd_wx0 + wHumPadd_w
wHum_hx0 = wTemp_hx1
wHum_wx1 = wHum_wx0 + wHum_wsize
wHum_hx1 = wHum_hx0 + wHum_hsize
draw.text((wHum_wx0, wHum_hx0), wHum,  fill=black, font=wHumFont)


# begin of Forecast boxes
for cfBox_col in range(fBox_cols):
    for cfBox_row in range(fBox_rows):
        cfBox_pos = (cfBox_row * fBox_cols) + cfBox_col

        slot = cfBox_pos + 1
        if slot >= len(fcast["list"]):
            break
        cfBox_data = get_owslot_dict(fcast, slot)

        # current forecast box boundaries
        cfBox_wx0 = f_wx0 + (cfBox_col * fBox_wx1)
        cfBox_hx0 = f_hx0 + (cfBox_row * fBox_hx1)
        cfBox_wx1 = cfBox_wx0 + fBox_wx1
        cfBox_hx1 = cfBox_hx0 + fBox_hx1
        draw.rectangle(((cfBox_wx0, cfBox_hx0), (cfBox_wx1, cfBox_hx1)), outline=black, width=1)  # outer border
        draw.line([(cfBox_wx1, cfBox_hx0), (cfBox_wx1, cfBox_hx1)], fill=black, width=1)  # right border
        draw.line([(cfBox_wx0, cfBox_hx1), (cfBox_wx1, cfBox_hx1)], fill=black, width=1)  # lower border
        # print("forecast box position {}, c {} / r {}: w0 {}, w1 {}, h0 {}, h1 {} ".format(cfBox_pos, cfBox_col, cfBox_row, cfBox_wx0, cfBox_wx1, cfBox_hx0,  cfBox_hx1))

        # current forecast box content
        cfBoxWi = ttfUnicode_from_iconId(cfBox_data['iconId'], cfBox_data['pod'], wiXmlMap)
        cfBoxHour = cfBox_data['time']
        cfBoxTemp = cfBox_data['temp']

        # text size
        cfBoxWi_w, cfBoxWi_h = fBoxWiFont.getsize(cfBoxWi)
        cfBoxHour_w, cfBoxHour_h = fBoxFont.getsize(cfBoxHour)
        cfBoxTemp_w, cfBoxTemp_h = fBoxFont.getsize(cfBoxTemp)
        cfBoxWiHalfPadding = (fBox_wx1 - (cfBoxWi_w + cfBoxTemp_w)) / 2

        # print weather icon
        # print("forecast weather icon size: width {}, height {}".format(cfBoxWi_w, cfBoxWi_h))
        cfBoxWi_rel_wx0 = cfBox_wx0 + int((cfBoxWiHalfPadding / 2))
        cfBoxWi_rel_hx0 = cfBox_hx0
        draw.text((cfBoxWi_rel_wx0, cfBoxWi_rel_hx0), cfBoxWi,  fill=black, font=fBoxWiFont)

        # print box's hour
        # print("forecast hour text size: width {}, height {}".format(cfBoxHour_w, cfBoxHour_h))
        cfBoxHour_rel_wx0 = cfBoxWi_rel_wx0 + cfBoxWi_h + int((cfBoxWiHalfPadding / 2))
        cfBoxHour_rel_hx0 = cfBox_hx0
        draw.text((cfBoxHour_rel_wx0, cfBoxHour_rel_hx0), cfBoxHour,  fill=black, font=fBoxFont)

        # print temp
        # print("forecast temp text size: width {}, height {}".format(cfBoxTemp_w, cfBoxTemp_h))
        cfBoxTemp_rel_wx0 = cfBoxWi_rel_wx0 + cfBoxWi_h + int((cfBoxWiHalfPadding / 2))
        cfBoxTemp_rel_hx0 = cfBox_hx0 + cfBoxHour_h
        draw.text((cfBoxTemp_rel_wx0, cfBoxTemp_rel_hx0), cfBoxTemp,  fill=black, font=fBoxFont)

# img_trans = img.transpose(Image.ROTATE_180)
img.show()
x = 0
# inky_display.set_image(img_trans)
# inky_display.show()
