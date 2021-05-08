#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser


class ConfigFile:
    def __init__(self, path=None):
        self.config = self.get_config(path)

    def get_config(self, path=None):
        config = configparser.ConfigParser()
        config_path = path if path else 'config.ini'
        config.read(config_path, encoding='utf-8')
        return config

    def get_continent_id(self, name):
        items = self.config['CONTINENTS'].items()
        continent_id = 0
        for k, v in items:
            if v == name:
                continent_id = k
                break
        return continent_id


if __name__ == "__main__":
    configFile = ConfigFile()
    config = configFile.config
    #print(config.sections())
    print(configFile.get_continent_id('AFC - Азия'))