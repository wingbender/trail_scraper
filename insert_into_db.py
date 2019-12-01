""" This file inputs new data into wikiloc scraper database
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project """

import pymysql
import config as cfg'

def insert_into_db(trails_data):
    """ Function that inserts "trail data" into trails, categories and users tables in database """
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        # TODO: create execute statements for trail_data and insert into trails, categories, and users
        # TODO: convert difficulty to integer rank
        # TODO: make sure to skip over duplicates / existing trails
        # TODO: add our own id index
        cur.execute("INSERT INTO trails () \
                                VALUES (?, ?, ?, ?, ?)", [])