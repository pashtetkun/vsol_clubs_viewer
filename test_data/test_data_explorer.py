#!/usr/bin/python
# -*- coding: utf-8 -*-
from gui.entities import entities

class TestDataExplorer:
    def __init__(self):
        pass

    def get_all_continents(self):
        return [entities.Continent(id=1, name='UEFA - Европа'),
                entities.Continent(id=2, name='AFC - Азия')]

    def get_countries(self, country_id):
        if country_id == 1:
            return [entities.Country(id=1, name='Андорра', continent_id=1),
                    entities.Country(id=2, name='Беларусь', continent_id=1)]
        if country_id == 2:
            return [entities.Country(id=5, name='Афганистан', continent_id=2),
                    entities.Country(id=6, name='Китай', continent_id=2),
                    entities.Country(id=7, name='Япония', continent_id=2)]

        return []