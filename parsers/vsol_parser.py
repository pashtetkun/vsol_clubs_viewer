#!/usr/bin/python
# -*- coding: utf-8 -*-
import lxml.html as html
from urllib.request import urlopen
import re
import os
from config_file import ConfigFile


class VsolParser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = config_file.config
        self.COUNTRIES_URL = self.config['VSOL']['countries_url']
        self.COUNTRY_URL = self.config['VSOL']['country_url']
        self.CLUB_URL = self.config['VSOL']['club_url']
        self.HIDDEN_TEAMS_URL = self.config['VSOL']['hidden_teams_url']

    def get_countries(self):
        countries = []
        page = html.parse(urlopen(self.COUNTRIES_URL))
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

    def get_club(self, vsol_id):
        url = "%s?num=%d" % (self.CLUB_URL, vsol_id)
        page = html.parse(urlopen(url))
        tables = page.getroot().xpath("//table[@class='wst nil']//table[@class='wst nil']")

        if not tables:
            club = {
                'name': 'Не существует',
                'stadium': '',
                'vsol_id': vsol_id
            }
            return club
        table = tables[0]
        div_name = table.xpath("//div[@class='tmhd']")[0]
        name = ''
        if (len(div_name.getchildren()) == 0):
            name = div_name.text_content()
        else:
            if (div_name.xpath("//span[@id='team_name']")):
                name = div_name.xpath("//span[@id='team_name']")[0].text_content()
            else:
                name = div_name.text_content()

        if (div_name.xpath("//span[@id='team_name']")):
            name = div_name.xpath("//span[@id='team_name']")[0].text_content()
        else:
            name = div_name.text_content()

        name = name.replace('\n', '').replace('\t', '')
        parent = div_name.getparent()
        stadiumText = parent.getchildren()[-3].text_content()
        pattern = re.compile('"[^\"]+"')
        stadium = re.findall(pattern, stadiumText)[0].strip('"')
        '''has_logo = False
        if (table.xpath("//a[@class='mnu']")):
            a = table.xpath("//a[@class='mnu']")[0]
            print(len(a))
            img = a.find("img")

        if (has_logo):
            print("%s?id=%d" % (LOGO_URL, vsol_id))'''

        club = {
            'name': name,
            'stadium': stadium,
            'vsol_id': vsol_id
        }
        return club

    def get_clubs(self, country_id):
        print('start getting clubs for country = %d' % country_id)
        clubs = []
        page = html.parse(urlopen("%s?num=%d" % (self.COUNTRY_URL, country_id)))
        table = None
        tables = page.getroot().find_class('tbl')

        '''
        for tbl in tables:
            if (len(tbl.getchildren()[0][0][0].getchildren()) == 0):
                continue
            if (tbl.getchildren()[0][0][0][0].text_content() == 'Название команды'):
                table = tbl
                break;
        '''
        filter_tables = []
        for tbl in tables:
            if tbl.attrib['width'] == '100%':
                filter_tables.append(tbl)
        table = filter_tables[-1]
        #c = table.attrib['align']

        ids = []
        rows = table.getchildren()
        for count, row in enumerate(rows):
            if ((count == 0) or (count == len(rows) - 1)):
                continue

            vsol_id = 0
            for i, col in enumerate(row):
                if (i == 0):
                    continue

                a = col.find_class('mnu')[0]
                href = a.attrib['href']
                vsol_id = int(href.split('=')[1])
                break

            ids.append(vsol_id)

        for id in ids:
            print('start getting club = %d' % id)
            club = self.get_club(id)
            club['is_hidden'] = False
            club['country_vsol_id'] = country_id
            clubs.append(club)
            print('end getting club = %d' % id)

        print('end getting clubs for country = %d' % country_id)
        return clubs

    def get_continent_id(self, country_id):
        print('start getting continent for country = %d' % country_id)
        page = html.parse(urlopen("%s?num=%d" % (self.COUNTRY_URL, country_id)))
        table = page.getroot().find_class('nil')[0]
        rows = table.getchildren()
        row = rows[0]
        col = row[1]
        name = col.text_content()
        return self.config_file.get_continent_id(name)

    def get_hidden_clubs(self):
        print('start getting hidden clubs')
        clubs = {}
        page = html.parse(urlopen("%s" % (self.HIDDEN_TEAMS_URL, )))
        select = page.getroot().find_class('form2 tct')[0]
        numbers = len(select.getchildren())
        countCl = 0
        ids = []
        for num in range(1, numbers+1):
            page = html.parse(urlopen("%s?page=%d&sort=1" % (self.HIDDEN_TEAMS_URL, num)))
            table = page.getroot().find_class('tbl')[0]
            rows = table.getchildren()
            for count, row in enumerate(rows):
                if ((count == 0) or (count == len(rows) - 1)):
                    continue
                name = ""
                country = ""
                vsol_id = 0
                for i, col in enumerate(row):
                    if (i > 1):
                        continue
                    if (i == 0):
                        a = col.find_class('mnu')[0]
                        #name = a.text_content()
                        href = a.attrib['href']
                        vsol_id = int(href.split('=')[1])
                    if (i == 1):
                        country = col.attrib['title']

                #club = {'name':name, 'vsol_id':vsol_id, 'is_hidden': True}
                countCl+=1
                if (country in clubs):
                    clubs.get(country).append(vsol_id)
                else:
                    clubs[country] = [vsol_id]
                print('get hidden club with vsol_id=%d' % vsol_id)

        return clubs


if __name__ == "__main__":
    dir_parsers = os.path.dirname(__file__)
    dir_root = os.path.dirname(dir_parsers)
    config_path = os.path.join(dir_root, 'config.ini')
    config_file = ConfigFile(config_path)
    vsol_parser = VsolParser(config_file)
    #print(vsol_parser.get_countries())
    #vsol_parser.get_clubs(4)
    #vsol_parser.get_clubs(6)
    #vsol_parser.get_clubs(214)
    #print(vsol_parser.get_club(12135))
    #vsol_parser.get_hidden_clubs()
    #print(vsol_parser.get_club(3045))
    #print(vsol_parser.get_club(3333))
    #print(vsol_parser.get_club(6188))
    #vsol_parser.get_club(23495)
    #print(vsol_parser.COUNTRIES_URL)
    vsol_country_id = 1
    print(vsol_parser.get_continent_id(vsol_country_id))
    print('Done')