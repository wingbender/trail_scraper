""" This file inputs new data into wikiloc scraper database
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project """

import pymysql

DB_FILENAME = 'trails.db'

def insert_into_db(trail_data):
    """ Function that inserts "trail data" into trails, categories and users tables in database """
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        # TODO: create execute statements for trail_data and insert into trails, categories, and users
        # TODO: convert difficulty to integer rank
        # TODO: make sure to skip over duplicates / existing trails
        # TODO: add our own id index
        for from_field, to_field in TRAIL_TO_DB_FIELDS.items():
        cur.execute("INSERT INTO trails (from_field) VALUES (