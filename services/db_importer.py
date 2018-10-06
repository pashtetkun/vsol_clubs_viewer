#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import os
from db_manager import db_manager


class DbImporter():
    def __init__(self):
        self.dbm = db_manager.DBManager()

    def import_countries(self, path):
        with open(os.path.join(os.getcwd(), path), 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.dbm.save_country(row[0], int(row[1]), int(row[2]))
        db_manager.db.close()


if __name__ == "__main__":
    importer = DbImporter()
    importer.import_countries('countries.csv')