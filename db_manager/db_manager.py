#!/usr/bin/python
# -*- coding: utf-8 -*-


from peewee import *

db = SqliteDatabase('vsol.db')


class Country(Model):
    name = CharField()
    vsol_id = IntegerField(unique=True)
    continent_id = IntegerField()

    class Meta:
        database = db


class DBManager():
    def __init__(self):
        db.connect()
        Country.create_table()

    def save_country(self, name, vsol_id, continent_id):
        country = Country.select().where(Country.vsol_id == vsol_id)
        if not country:
            Country.create(name=name, vsol_id=vsol_id, continent_id=continent_id)
