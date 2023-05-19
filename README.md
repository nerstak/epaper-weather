# ePaper-Weather

## Description

![IMG20230505162319-01](https://github.com/nerstak/epaper-weather/assets/33179821/0891a2b7-28ef-4423-9af8-17cc1ae9a916)

A program to display weather and other useless information you could get by looking at the window

### Technologies used

Software:

- Python3
- Waveshare e-paper [lib](https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/)

Additional and optional infrastructure:

- InfluxDB
- Grafana

Hardware (you are not required to use the exact same one, but you'll need to adapt the program):

- Raspberry Pi 3A+ (I had some lying around)
- [Waveshare 2.13inch e-paper](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual)
- DHT22 sensor, for humidity and temperature

Minimal hardware requirements:

- Microcontroller with:
    - GPIO
    - Ability to connect to Internet
- Whatever e-paper screen (may require some adaptations)

### Features

- Display current weather (temperature, humidity, rain)
- Display 24hours forecast
- Display sunrise and sunset time
- Display temperature and humidity from sensor (optional)
- Log data into InfluxDB (optional)

## Usage

### Installation

#### InfluxDB

Optionally, install an InfluxDB (1.8 for 32bits RaspberryPi).

You will need to create a Database (no credential used here).

#### Grafana

Optionally, install Grafana.

Follow this [guide](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/) from *Installation* part.
Add a Datasource, select InfluxDB and put `http://localhost:8086`.

#### OpenWeather

Go to [OpenWeather](https://openweathermap.org/price#current), create an account and create a key for the Professional
Collection Free Tier. This tier **does not** require a credit card.

#### ePaper Weather

Download the `lib` folder
from [waveshare repository](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd),
and put it at the root of the project

#### config.yaml

Copy the file `config.example.yaml` and name the new file `config.yaml`. Inside, you will need to configure the
following elements:

- `API_KEY`: The OpenWeather key you created just before. This **your** personal key, it won't leave you device
- `unit`: `metric` or `imperial`
- `coordinates`: Coordinates of the place you want to track the weather of. Use this website for
  help: [LatLong.net](https://www.latlong.net/)
- `refresh_period_min`: How often to refresh the data or the screen in minutes (`data` being lower than `screen` will
  have no effect)
- `city`: Name of the location of the place you are tracking the weather of. OpenWeather API does not always give a
  relevant city name
- `metrics`: If you wish to monitor data. Set `record_metrics` to `false` or `true`. Set `database_url`
  and `database_name` to the one setup during InfluxDB installation.

Run `pip install -Ur requirements.txt`, `sudo apt-get install libgpiod2`

#### Service (auto-run)

Copy the file `systemd/epaper-weather.example.service` and name the new file `systemd/epaper-weather.service`. Inside, you will need to configure the
following elements:
- `User`: Put your own user
- `PATH_TO_PROJECT`: Path of your project location

```
sudo cp systemd/epaper-weather.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable epaper-weather
sudo systemctl start epaper-weather
```

## Related projects

Some projects that helped me overcome some issues:

- [inkyWeather](https://github.com/xenOs76/inkyWeather): a similar project with Inky pHAT. I borrowed some graphical
  parts to speed up the development process
- [E-paper Weather Display](https://github.com/AbnormalDistributions/e_paper_weather_display): a similar project with a
  bigger screen
