#!/usr/bin/python
# -*- coding: utf-8 -*-
import lxml.html as html


COUNTRIES_URL = 'http://virtualsoccer.ru/teams.php'


class VsolParser:
    def __init__(self):
        pass

    def get_countries(self):
        countries = []
        page = html.parse(COUNTRIES_URL)
        table = page.getroot().find_class('tbl')[0]
        rows = table.getchildren()
        for count, row in enumerate(rows):
            if ((count < 2) or (count == len(rows) - 1)):
                continue

            name = ''
            vsol_id = 0
            for i, col in enumerate(row):
                if (i > 1):
                    continue

                if (i == 0):
                    name = col.attrib['title']

                if (i == 1):
                    href = col.getchildren()[0].find('a').attrib['href']
                    vsol_id = int(href.split('=')[1])

            countries.append({
                'name': name,
                'vsol_id': vsol_id
            })

        return countries

if __name__ == "__main__":
    vsol_parser = VsolParser()
    print(vsol_parser.get_countries())