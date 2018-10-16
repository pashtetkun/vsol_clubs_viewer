#!/usr/bin/python
# -*- coding: utf-8 -*-
from gui.entities import entities
from db_manager import db_manager
from services import vsol_exporter
import os
import csv


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

    def get_clubs(self, country_vsol_id):
        return db_manager.Club.select()\
                              .order_by(db_manager.Club.name)\
                              .where(db_manager.Club.country_vsol_id == country_vsol_id)

    def update_clubs(self, clubs):
        for club in clubs:
            self.dbm.save_club(club["name"], club["vsol_id"], club["country_vsol_id"], club["stadium"],
                              club["is_hidden"])

    def import_countries(self, path):
        with open(os.path.join(os.getcwd(), path), 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.dbm.save_country(row[0], int(row[1]), int(row[2]))
        db_manager.db.close()


if __name__ == "__main__":
    explorer = DataExplorer()
    explorer.import_countries('countries.csv')