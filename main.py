#!/usr/bin/python
# -*- coding: utf-8 -*-
from config_file import ConfigFile
from gui import main_window

if __name__ == "__main__":
    config_file = ConfigFile()
    main_window.MainWindow(1000, 500, 'logo.ico', 'logo.gif', config_file)
