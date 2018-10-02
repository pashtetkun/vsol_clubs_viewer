#!/usr/bin/python
# -*- coding: utf-8 -*-
from parsers import vsol_parser
import csv
import os


class VsolExporter:
    def __init__(self):
        pass

    def countriesToCSV(self):
        parser = vsol_parser.VsolParser()
        countries = parser.get_countries()

        csv_file = os.path.join(os.getcwd(), 'countries.csv')
        with open(csv_file, "w", encoding='utf-8') as output:
            writer = csv.writer(output, lineterminator='\n', delimiter=';')
            for country in countries:
                writer.writerow([country['name'], country['vsol_id']])


if __name__ == "__main__":
    vsol_exporter = VsolExporter()
    vsol_exporter.countriesToCSV()