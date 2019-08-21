import os
import yaml


def get_config(parameter_name):
    home = os.getcwd()
    config_file_path = os.path.join(home, 'telegram_bot_config.yml')
    with open(config_file_path, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    try:
        return cfg[parameter_name]
    except:
        return False
