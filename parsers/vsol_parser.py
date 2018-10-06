#!/usr/bin/python
# -*- coding: utf-8 -*-
import lxml.html as html
import re


COUNTRIES_URL = 'http://virtualsoccer.ru/teams.php'
COUNTRY_URL = 'http://virtualsoccer.ru/teams_cntr.php'
CLUB_URL = 'http://virtualsoccer.ru/roster.php'
HIDDEN_TEAMS_URL = 'http://virtualsoccer.ru/teams_hidden.php'


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

    def get_club(self, vsol_id):
        page = html.parse("%s?num=%d" % (CLUB_URL, vsol_id))
        table = page.getroot().xpath("//table[@class='wst nil']//table[@class='wst nil']")[0]
        div_name = table.xpath("//div[@class='tmhd']")[0]
        if (len(div_name.getchildren()) == 0):
            name = div_name.text_content()
        else:
            if (div_name.xpath("//span[@id='team_name']")):
                name = div_name.xpath("//span[@id='team_name']")[0].text_content()
            else:
                name = div_name.text_content()

        parent = div_name.getparent()
        stadiumText = parent.getchildren()[-3].text_content()
        # print(vsol_id, stadiumText)
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
        clubs = []
        page = html.parse("%s?num=%d" % (COUNTRY_URL, country_id))
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
        table = tables[0]

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
            club = self.get_club(id)
            club['isHidden'] = False
            clubs.append(club)
            print(id)

        return clubs


if __name__ == "__main__":
    vsol_parser = VsolParser()
    #print(vsol_parser.get_countries())
    #vsol_parser.get_clubs(4)
    #print(vsol_parser.get_club(12135))
    print('Done')