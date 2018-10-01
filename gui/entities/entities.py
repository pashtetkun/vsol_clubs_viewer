#!/usr/bin/python
# -*- coding: utf-8 -*-


class Continent:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Country:
    def __init__(self, id, name, continent_id):
        self.id = id
        self.name = name
        self.continent_id


class Club:
    def __init__(self, id, name, hidden, country_id):
        self.id = id
        self.name = name
        self.hidden = hidden
        self.country_id = country_id
