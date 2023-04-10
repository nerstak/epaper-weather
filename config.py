import yaml
from yaml import SafeLoader


def load_config(cfg):
    with open(cfg, 'r') as f:
        data = yaml.load(f, Loader=SafeLoader)
        return data


CONFIG = load_config("config.yaml")
