#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'c:/python391/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'c:/python391/tcl/tk8.6'

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages = ["tkinter", "peewee"],
    excludes = [],
    includes = [],
    include_files=['c:/python391/DLLs/tcl86t.dll',
                   'c:/python391/DLLs/tk86t.dll',
                   #'C:\\Windows\\System32\\ucrtbase.dll']
                   'c:/python391/DLLs/sqlite3.dll',
                   os.path.join(os.getcwd(), 'logo.ico'),
                   os.path.join(os.getcwd(), 'logo.gif')]
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
