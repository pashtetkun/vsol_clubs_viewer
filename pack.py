#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import configparser
from cx_Freeze import setup, Executable

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(),'config.ini'), encoding='utf-8')
PYTHON_DIR = config['python']['python_dir']
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl/tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl/tk8.6')

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages = ["tkinter", "peewee"],
    excludes = [],
    includes = [],
    include_files=[os.path.join(PYTHON_DIR, 'DLLs/tcl86t.dll'),
                   os.path.join(PYTHON_DIR, 'DLLs/tk86t.dll'),
                   #'C:\\Windows\\System32\\ucrtbase.dll']
                   os.path.join(PYTHON_DIR, 'DLLs/sqlite3.dll'),
                   os.path.join(os.getcwd(), 'logo.ico'),
                   os.path.join(os.getcwd(), 'logo.gif'),
                   os.path.join(os.getcwd(), 'config.ini')]
)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base = base)
]

setup(
    name = "App",
    version = "0.1",
    description = "test",
    options = {"build_exe": buildOptions},
    executables = executables)
