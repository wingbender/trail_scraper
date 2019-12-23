""" flickr_db: script to extract images from Flickr API for trails in database for Wikiloc Scraper
authors: Roi Weinberger & Sagiv Yaari. Date: December 2019 """

import sys
import pymysql
from argparse import ArgumentParser
from db_handler import get_connection
from flickrAPI import Flickr

class ArgParser(ArgumentParser):
    """ Class of argument parser functions. Child class of ArgumentParser from argparse module"""
    def __init__(self):
        super().__init__(description='Wikiloc.com scraper')

        self.add_argument('-p', metavar='no. of photos to extract', type=int, default=1,
                            help='Enter the number of photos to extract from Flickr API. Defaults to 1')
        self.add_argument('-c', '--country', type=str, default='España',
                          metavar="country to get images urls. Defaults to 'España' (Spain)")
        self.args = []

    def get_args(self):
        """ Save arguments and parse them from the CLI """
        self.args = self.parse_args()

def get_trail_ids(country):
    """Fucntion returns a list from the MySQL database of all trail_id in a given country"""
    with conn.cursor() as cursor:
        query = f"SELECT trail_id, start_lon as lon, start_lat as lat " \
                f"FROM trails.trails WHERE country='{pymysql.escape_string(country)}';"
        cursor.execute(query)
        result = cursor.fetchall()
        if result is None:
            print(f'No trails in {country} found in database')
            exit()
        else:
            return list(result)

def update_image(trail_id, image_urls):
    """Update database photo_urls field with image_urls list by specific trail_id"""
    with conn.cursor() as cursor:
        query = f"UPDATE trails.trails " \
                f"SET photo_urls=" \
                f"'{pymysql.escape_string(';'.join(pymysql.escape_string(url) for url in image_urls))}' " \
                f"WHERE trail_id={trail_id};"
        cursor.execute(query)


if __name__ == '__main__':
    ap = ArgParser()
    ap.get_args()

    conn = get_connection()
    data = get_trail_ids(ap.args.country)
    flickr = Flickr()
    for row in data:
        try:
            image_urls = flickr.get_photos_url(row['lat'], row['lon'], radius=5, no_of_photos=ap.args.p)
        except Exception as e:
            print(f"Failed to retrieve images urls for trail {row['trail_id']}")
            print(e)
            continue
        try:
            update_image(row['trail_id'], image_urls)
            print(f"Retrieved images urls and update database for trail {row['trail_id']}")
        except Exception as e:
            print(f"Failed to update database for trail {row['trail_id']}")
            print(e)
            continue
    conn.commit()
    conn.close()
