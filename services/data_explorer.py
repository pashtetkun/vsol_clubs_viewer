#!/usr/bin/python
# -*- coding: utf-8 -*-
from config_file import ConfigFile
from gui.entities import entities
from db_manager import db_manager
from services import vsol_exporter
import os
import csv


class DataExplorer():
    def __init__(self, config_file, db_path):
        self.config_file = config_file
        self.config = config_file.config
        db_path = db_path if db_path else 'vsol.db'
        self.dbm = db_manager.DBManager(db_path)
        self.exporter = vsol_exporter.VsolExporter(self.config_file)

    def get_all_continents(self):
        continents = []
        for (each_key, each_val) in self.config.items('CONTINENTS'):
            continents.append(entities.Continent(id=each_key, name=each_val))
        return continents

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
    dir_services = os.path.dirname(__file__)
    dir_root = os.path.dirname(dir_services)
    config_path = os.path.join(dir_root, 'config.ini')
    config_file = ConfigFile(config_path)
    explorer = DataExplorer(config_file, 'c:/1/vsol.db')
    #explorer.import_countries('countries.csv')
    #countries = explorer.get_all_countries()
    #for country in countries:
        #print(country)
    #print(explorer.get_all_continents())
