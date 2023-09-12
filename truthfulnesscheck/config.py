import os
import yaml


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as config_file:
        try:
            return yaml.safe_load(config_file)
        except yaml.YAMLError as ex:
            print(ex)


config = load_config()
