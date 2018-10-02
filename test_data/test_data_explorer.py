#!/usr/bin/python
# -*- coding: utf-8 -*-
from gui.entities import entities

class TestDataExplorer:
    def __init__(self):
        pass

    def get_all_continents(self):
        return [entities.Continent(id=1, name='UEFA - Европа'),
                entities.Continent(id=2, name='AFC - Азия')]

    def get_countries(self, continent_id):
        if continent_id == 1:
            return [entities.Country(id=1, name='Андорра', continent_id=1),
                    entities.Country(id=2, name='Беларусь', continent_id=1)]
        if continent_id == 2:
            return [entities.Country(id=5, name='Афганистан', continent_id=2),
                    entities.Country(id=6, name='Китай', continent_id=2),
                    entities.Country(id=7, name='Япония', continent_id=2)]

        return []

    def get_clubs(self, country_id):
        if country_id == 1:
            return [entities.Club(id=1, name="Интер (Эскальдес, Андорра)", hidden=False, country_id=1),
                    entities.Club(id=2, name="Спортинг (Эскальдес, Андорра)", hidden=True, country_id=1)]
        if country_id == 2:
            return [entities.Club(id=3, name="Торпедо (Минск, Беларусь)", hidden=False, country_id=2),
                    entities.Club(id=4, name="Щучин (Щучин, Беларусь)", hidden=True, country_id=2)]
        return []