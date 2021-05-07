#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser


class ConfigFile:
    def __init__(self):
        pass

    def get_config(self, path=None):
        config = configparser.ConfigParser()
        config_path = path if path else 'config.ini'
        config.read(config_path, encoding='utf-8')
        return config


if __name__ == "__main__":
    config = ConfigFile().get_config()
    print(config.sections())