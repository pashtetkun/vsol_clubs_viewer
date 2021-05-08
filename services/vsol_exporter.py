#!/usr/bin/python
# -*- coding: utf-8 -*-
from config_file import ConfigFile
from parsers import vsol_parser
import csv
import os


class VsolExporter:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = config_file.config
        self.parser = vsol_parser.VsolParser(config_file)

    def countries_to_csv(self):
        countries = self.parser.get_countries()

        csv_file = os.path.join(os.getcwd(), 'countries.csv')
        with open(csv_file, "w", encoding='utf-8') as output:
            writer = csv.writer(output, lineterminator='\n', delimiter=';')
            for country in countries:
                writer.writerow([country['name'], country['vsol_id']])
        return csv_file

    def countries_to_csv2(self):
        countries = self.parser.get_countries()
        csv_file = os.path.join(os.getcwd(), 'countries.csv')
        with open(csv_file, "w", encoding='utf-8') as output:
            writer = csv.writer(output, lineterminator='\n', delimiter=';')
            for country in countries:
                continent_id = self.parser.get_continent_id(country['vsol_id'])
                writer.writerow([country['name'], country['vsol_id'], continent_id])
        return csv_file

    def get_clubs(self, countries):
        all_clubs = []
        #countries = self.de.get_all_countries()
        for country in countries:
            clubs = self.parser.get_clubs(country.vsol_id)
            all_clubs.extend(clubs)
        #for club in all_clubs:
            #self.de.save_club(club["name"], club["vsol_id"], club["country_vsol_id"], club["stadium"],
                              #club["is_hidden"])
        return all_clubs


if __name__ == "__main__":
    dir_services = os.path.dirname(__file__)
    dir_root = os.path.dirname(dir_services)
    config_path = os.path.join(dir_root, 'config.ini')
    config_file = ConfigFile(config_path)
    vsol_exporter = VsolExporter(config_file)
    vsol_exporter.countries_to_csv2()