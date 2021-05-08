#!/usr/bin/python
# -*- coding: utf-8 -*-


from peewee import *

db = SqliteDatabase(None)


class Country(Model):
    name = CharField()
    vsol_id = IntegerField(unique=True)
    continent_id = IntegerField()

    class Meta:
        database = db


class Club(Model):
    name = CharField()
    vsol_id = IntegerField(unique=True)
    country_vsol_id = IntegerField()
    stadium = CharField()
    hidden = BooleanField()

    class Meta:
        database = db


class DBManager():
    def __init__(self, path):
        db.init(path)
        db.connect()
        Country.create_table()
        Club.create_table()

    def save_country(self, name, vsol_id, continent_id):
        country = Country.select().where(Country.vsol_id == vsol_id)
        if not country:
            Country.create(name=name, vsol_id=vsol_id, continent_id=continent_id)

    def save_club(self, name, vsol_id, country_vsol_id, stadium, hidden):
        club = Club.get_or_none(Club.vsol_id == vsol_id)
        if not club:
            Club.create(name=name, vsol_id = vsol_id, country_vsol_id = country_vsol_id, stadium = stadium,
                                hidden = hidden)
