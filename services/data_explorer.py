#!/usr/bin/python
# -*- coding: utf-8 -*-
from gui.entities import entities
from db_manager import db_manager
from services import vsol_exporter


class DataExplorer():
    def __init__(self):
        self.dbm = db_manager.DBManager()
        self.exporter = vsol_exporter.VsolExporter()

    def get_all_continents(self):
        return [entities.Continent(id=1, name='UEFA - Европа'),
                entities.Continent(id=2, name='AFC - Азия'),
                entities.Continent(id=3, name='CAF - Африка'),
                entities.Continent(id=4, name='CONCACAF - Сев. Америка'),
                entities.Continent(id=5, name='CONMEBOL - Южн. Америка')]

    def get_countries(self, continent_id):
        return db_manager.Country.select()\
                          .order_by(db_manager.Country.name)\
                          .where(db_manager.Country.continent_id == continent_id)

    def get_all_countries(self):
        return db_manager.Country.select().order_by(db_manager.Country.name)

    def get_clubs(self, country_id):
        return []

    def update_clubs(self, clubs):
        pass