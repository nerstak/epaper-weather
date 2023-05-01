import logging
import os

import yaml
from yaml import SafeLoader

log = logging.getLogger("epaper_weather")
logging.basicConfig(level=logging.INFO)

def load_config(cfg):
    with open(cfg, 'r') as f:
        data = yaml.load(f, Loader=SafeLoader)
        return data


full_path = os.path.realpath(__file__)
workdir = os.path.dirname(full_path)

CONFIG = load_config(workdir + "/config.yaml")

wakeup_time_s = 60
