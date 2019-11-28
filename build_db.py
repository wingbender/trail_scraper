""" This file creates the databases and tables for wikiloc scraper data
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project """


import pymysql
from getpass import getpass


def test_sql_connection():
    username = 'root'
    prompt = f'enter password for user {username}: '
    password = getpass(prompt=prompt)
    con = pymysql.connect(user=username, password=password)
    cur = con.cursor()
    cur.execute("SELECT now()")
    now = cur.fetchone()
    print("Database time: {}".format(now[0]))
    cur = con.cursor()
    cur.execute("SELECT user()")
    user = cur.fetchone()
    print("Database user: {}".format(user[0]))
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print("Database version: {}".format(version[0]))


def create_database():

# import sqlite3
# import os
#
# DB_FILENAME = 'trails.db'
#
# if os.path.exists(DB_FILENAME):
#     os.remove(DB_FILENAME)
#
# with sqlite3.connect(DB_FILENAME) as con:
#     cur = con.cursor()
#     # TODO: add autoincrement to primary key
    cur.execute('''CREATE TABLE trails (
                        id INT PRIMARY KEY , #
                        wikiloc_id INT,
                        title TEXT,
                        url TEXT,
                        user_id INT,
                        category_id INT,
                        country TEXT,
                        distance FLOAT,
                        loop BOOL,
                        elevation_gain_uphill FLOAT,
                        elevation_max FLOAT,
                        elevation_gain_downhill FLOAT,
                        elevation_min FLOAT,
                        moving_time INT,
                        time INT,
                        uploaded_date TEXT,
                        recorded_date TEXT,
                        no_coords INT,
                        difficulty INT
                        )''')

    cur.execute('''CREATE TABLE categories (
                        category_id PRIMARY KEY,
                        category_name TEXT,
                        FOREIGN KEY(category_id) REFERENCES trails(category_id))
                        )''')

    cur.execute('''CREATE TABLE users (
                        user_id PRIMARY KEY,
                        user_name TEXT,
                        FOREIGN KEY(user_id) REFERENCES trails(user_id))
                        )''')
#
#     cur.close()

if __name__ == '__main__':
    test_sql_connection()
