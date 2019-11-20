""" This file inputs new data into wikiloc scraper database
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project """

import sqlite3

DB_FILENAME = 'trails.db'

def insert_into_db(trail_data):
    """ Function that inserts "trail data" into trails, categories and users tables in database """
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        # TODO: create execute statements for trail_data and insert into trails, categories, and users
        # TODO: convert difficulty to integer rank
        # TODO: make sure to skip over duplicates / existing trails
        cur.execute("INSERT INTO trails () \
                                VALUES (?, ?, ?, ?, ?)", [])