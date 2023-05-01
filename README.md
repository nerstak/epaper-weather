# ePaper-Weather

## Description

A program to display weather and other useless information you could get by looking at the window

### Technologies used

Software:

- Python3
- Waveshare e-paper [lib](https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/)

Additional infrastructure:

- [TickTock](https://github.com/ytyou/ticktock)
- Grafana

Hardware (you are not required to use the exact same one, but you'll need to adapt the program):

- Raspberry Pi 3A+ (I had some lying around)
- [Waveshare 2.13inch e-paper](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual)

Minimal hardware requirements:

- Microcontroller with:
    - GPIO
    - Ability to connect to Internet
- Whatever e-paper screen (may require some adaptations)

### Features

TODO

## Usage

### Installation

#### TickTock

[TickTock](https://github.com/ytyou/ticktock) is a lightweight time-series database. Is it production ready? Maybe not,
but I didn't want something heavy like Prometheus, Influx or else.

`curl -L -o  ticktok.tar.gz https://github.com/ylin30/ticktock-wiki/raw/master/binaries/ticktock.0.11.1-rpi-32bit.tar.gz`
`tar xvf ticktok.tar.gz`
`sudo cp ticktock.service /etc/systemd/system`
`sudo systemctl enable ticktock`

#### Grafana

Follow this [guide](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/) from *Installation* part.
Add a Datasource, select OpenTSDB and put `http://localhost:6182`.

#### OpenWeather

Go to [OpenWeather](https://openweathermap.org/price#current), create an account and create a key for the Professional
Collection Free Tier. This tier **does not** require a credit card.

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

#### Service (auto-run)

TODO

## Related projects
Some projects that helped me overcome some issues: 
- [inkyWeather](https://github.com/xenOs76/inkyWeather): a similar project with Inky pHAT. I borrowed some graphical parts
- [E-paper Weather Display](https://github.com/AbnormalDistributions/e_paper_weather_display): a similar project with a bigger screen
