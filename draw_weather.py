import math
from datetime import datetime

from PIL import ImageFont, Image, ImageDraw

from config import workdir, CONFIG
from epd_handler import draw_image_on_hardware, screenWidth, screenHeight
from ttf import icon_to_unicode, icon_id_to_unicode_ttf, get_text_size

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

# 180° rotated display
w_wx0 = 0  # current weather area: start width
w_hx0 = 0  # current weather area: start height
w_wx1 = screenWidth  # current weather area: end width
w_hx1 = int(screenHeight / 2)  # current weather area: end height

f_wx0 = 0  # forecast area: start width
f_hx0 = w_hx1  # forecast area: start height
f_wx1 = screenWidth  # forecast area: end width
f_hx1 = int(screenHeight / 2)  # forecast area: end height

forecast_boxes_row = 2
forecast_boxes_col = 4
fBox_wx1 = math.floor(w_wx1 / forecast_boxes_col)
fBox_hx1 = math.floor(f_hx1 / forecast_boxes_row)


def _current_time():
    """
    Format current time (hour & minutes)
    :return: str
    """
    return datetime.now().strftime('%H:%M')


def _current_date():
    """
    Format current date
    :return: str
    """
    return datetime.now().strftime('%a, %b %d')


def draw_weather_image(weather, fcast: dict):
    img = Image.new("L", (screenWidth, screenHeight), 255)
    draw = ImageDraw.Draw(img)

    draw_current_weather(draw, weather)
    draw_forecast_boxes(draw, fcast)
    img_rotated = img.transpose(Image.ROTATE_180)
    draw_image_on_hardware(img_rotated)
    img_rotated.close()


def draw_forecast_boxes(draw, fcast):
    """
    Draw all forecast boxes
    :param draw: Image with drawing
    :param fcast: Forecast data
    """
    for fcast_col in range(forecast_boxes_col):
        for fcast_row in range(forecast_boxes_row):
            box_pos = (fcast_row * forecast_boxes_col) + fcast_col

            slot = box_pos + 1
            if slot >= len(fcast["list"]):
                break
            forecast_data = format_data(fcast, slot)

            draw_forecast_box(forecast_data, fcast_col, fcast_row, draw)


def draw_forecast_box(forecast_data, box_col, box_row, draw):
    """
    Draw a single forecast box
    :param forecast_data: Forecast data
    :param box_col: Number of colum
    :param box_row: Number of row
    :param draw: Image with drawing
    """

    # Forecast box boundaries
    box_wx0 = f_wx0 + (box_col * fBox_wx1)
    box_hx0 = f_hx0 + (box_row * fBox_hx1)
    box_wx1 = box_wx0 + fBox_wx1
    box_hx1 = box_hx0 + fBox_hx1
    draw.rectangle(((box_wx0, box_hx0), (box_wx1, box_hx1)), outline=black, width=1)
    draw.line([(box_wx1, box_hx0), (box_wx1, box_hx1)], fill=black, width=1)
    draw.line([(box_wx0, box_hx1), (box_wx1, box_hx1)], fill=black, width=1)

    # Loading data
    weather_icon = icon_id_to_unicode_ttf(forecast_data['iconId'], forecast_data['pod'], wiXmlMap)
    hour_text = forecast_data['time']
    temperature_text = forecast_data['temp']

    # Text size
    ico_width, ico_height = get_text_size(draw=draw, text=weather_icon, font=fBoxWiFont)
    hour_width, hour_height = get_text_size(draw=draw, text=hour_text, font=fBoxFont)
    temp_width, temp_height = get_text_size(draw=draw, text=temperature_text, font=fBoxFont)

    width_padding = (fBox_wx1 - (ico_width + temp_width)) / 2
    height_padding = (fBox_hx1 - (hour_height + temp_height)) / 2

    # Print Weather Icon
    ico_rel_wx0 = box_wx0 + int((width_padding / 2))
    ico_rel_hx0 = box_hx0
    draw.text((ico_rel_wx0, ico_rel_hx0), weather_icon, fill=black, font=fBoxWiFont)

    # Print Time
    hour_rel_wx0 = ico_rel_wx0 + ico_width + int((width_padding / 2))
    hour_rel_hx0 = box_hx0
    draw.text((hour_rel_wx0, hour_rel_hx0), hour_text, fill=black, font=fBoxFont)

    # Print Temperature
    temp_rel_wx0 = ico_rel_wx0 + ico_width + int((width_padding / 2))
    temp_rel_hx0 = box_hx0 + hour_height + height_padding
    draw.text((temp_rel_wx0, temp_rel_hx0), temperature_text, fill=black, font=fBoxFont)


def draw_current_weather(draw, weather):
    """
    Draw current weather info
    :param draw: Pillow Draw
    :param weather: Data about weather
    """
    left_padding = 5

    # Date & Time
    hour_wx0, hour_hx0, hour_wx1, hour_hx1 = draw.textbbox(xy=(left_padding, 0), text=_current_time(), font=clockFont)
    date_wx0, date_hx0, date_wx1, date_hx1 = draw.textbbox(xy=(left_padding, hour_hx1), text=_current_date(),
                                                           font=dateFont)
    draw.text((left_padding, 0), _current_time(), fill=black, font=clockFont)
    draw.text((left_padding, hour_hx1), _current_date(), fill=black, font=dateFont)

    # Current weather
    city_text = CONFIG.get("city", weather["name"])
    temperature_text = weather["main"]["temp"]
    temp_feels_text = weather["main"]["feels_like"]
    humidity_text = weather["main"]["humidity"]
    description_text = weather["weather"][0]["description"]

    sunrise_text = datetime.fromtimestamp(weather["sys"]["sunrise"]).strftime('%H:%M')
    sunset_text = datetime.fromtimestamp(weather["sys"]["sunset"]).strftime('%H:%M')

    weather_ico_code = weather["weather"][0]["icon"]

    # Weather Icon
    weather_icon_unicode = icon_to_unicode(weather_ico_code, wiXmlMap)
    ico_wx0, ico_hx0, ico_wx1, ico_hx1 = draw.textbbox(xy=(hour_wx1 + left_padding, 0),
                                                       text=weather_icon_unicode, font=wIcoFont)
    draw.text((ico_wx0, 0), weather_icon_unicode, fill=black, font=wIcoFont)

    # City Name
    city_and_desc_hx0 = max(ico_hx1, date_hx1) + left_padding
    city_wx0, city_hx0, city_wx1, city_hx1 = draw.textbbox(xy=(left_padding, city_and_desc_hx0), text=city_text,
                                                           font=wCityFont)
    draw.text((city_wx0, city_and_desc_hx0), city_text, fill=black, font=wCityFont)

    # Description Weather
    desc_wx0, desc_hx0, desc_wx1, desc_hx1 = draw.textbbox(xy=(ico_wx0, city_and_desc_hx0), text=description_text,
                                                           font=wDetFont)
    draw.text((ico_wx0, city_and_desc_hx0), description_text, fill=black, font=wDetFont)

    # Temperature
    temperature_text = str(math.ceil(temperature_text)) + "°C"
    temperature_wx0, temperature_hx0, temperature_wx1, temperature_hx1, = draw.textbbox(xy=(ico_wx1, 5),
                                                                                        text=temperature_text,
                                                                                        font=wTempFont)

    values_wx0 = max(ico_wx1, desc_wx1)
    values_size_available = int((w_wx1 - values_wx0) / 2)

    temperature_padding = int(((values_size_available - (temperature_wx1 - temperature_wx0)) / 2))
    draw.text((temperature_wx0 + temperature_padding, 5), temperature_text, fill=black, font=wTempFont)

    # Humidity
    humidity_text = str(humidity_text) + "%"
    humidity_wx0, humidity_hx0, humidity_wx1, humidity_hx1 = draw.textbbox(xy=(ico_wx1, temperature_hx1),
                                                                           text=humidity_text, font=wHumFont)
    humidity_padding = int(((values_size_available - (humidity_wx1 - humidity_wx0)) / 2))
    draw.text((humidity_wx0 + humidity_padding, temperature_hx1), humidity_text, fill=black, font=wHumFont)

    # Feels Temperature
    temp_feels_text = " => " + str(math.ceil(temp_feels_text)) + "°C"
    _, _ = get_text_size(draw=draw, text=temp_feels_text, font=wTempFont)

    draw.text((temperature_wx1 + temperature_padding, 5), temp_feels_text, fill=black, font=wTempFont)

    if w_hx1 - city_hx1 > 25:
        sunrise_icon = icon_id_to_unicode_ttf('sunrise', '', wiXmlMap)
        sunset_icon = icon_id_to_unicode_ttf('moonrise', '', wiXmlMap)

        l_ico, _ = get_text_size(draw=draw, text=sunrise_icon, font=fBoxWiFont)
        draw.text(xy=(5, w_hx1 - 25), text=sunrise_icon, font=fBoxWiFont, fill=black)

        l_sunset, _ = get_text_size(draw=draw, text=sunrise_text, font=wTempFont) + l_ico
        draw.text(xy=(5 + l_ico + 2, w_hx1 - 22), text=sunrise_text, font=wTempFont, fill=black)

        l_ico, _ = get_text_size(draw=draw, text=sunset_icon, font=fBoxWiFont)
        draw.text(xy=(l_sunset + 5 * 4, w_hx1 - 25), text=sunset_icon, font=fBoxWiFont, fill=black)
        draw.text(xy=(l_sunset + 5 * 4 + l_ico + 2, w_hx1 - 22), text=sunset_text, font=wTempFont, fill=black)


def draw_error(exception: Exception):
    """
    Draw an error image
    :param exception: Exception
    """
    error_image = Image.new('1', (screenWidth, screenHeight), 255)
    draw = ImageDraw.Draw(error_image)

    draw.text((0, 0), "ERROR", font=clockFont, fill=black)
    draw.text((0, 50), str(exception), font=dateFont, fill=black)
    draw.text((0, 70), 'Retrying in a minute', font=dateFont, fill=black)
    draw.text((0, 80), 'Last Refresh: ' + str(_current_time()) + " " + str(_current_date()), font=dateFont, fill=black)
    img_rotated = error_image.transpose(Image.ROTATE_180)
    draw_image_on_hardware(img_rotated)
    img_rotated.close()


def format_data(fcast_json, slot):
    """
    Format the data into a dict
    :param fcast_json: JSON
    :param slot: Slot of array to load data from
    :return:
    """

    data = {}
    fcast_data = fcast_json['list'][slot]
    temp = math.ceil(fcast_data['main']['temp'])
    temp_feel = math.ceil(fcast_data['main']['feels_like'])
    hum = math.ceil(fcast_data['main']['humidity'])
    dt = datetime.utcfromtimestamp(fcast_data['dt'])

    data['temp'] = str(temp) + "°C"
    data['temp_feel'] = str(temp_feel) + "°C"
    data['hum'] = str(hum) + "%"
    data['iconId'] = str(fcast_data['weather'][0]['id'])
    data['pod'] = str(fcast_data['sys']['pod'])
    data['time'] = dt.strftime("%H:%M")
    return data
