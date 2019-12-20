""" entry point for wikiloc scraper to scrape trail data from wikiloc.com
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project

    The main function runs with command line arguments to scrape a range of files from a single category
    or loops through all the categories to scrape the entire site.

    command line arguments are:

    [-h] : show help message
    [-c category to scrape int]: category to scrape by number
    [-C category to scrape string]: category to scrape by name
    [-r trails range]: range of trails to scrape e.g.: '14-76'
    [-f]: extracts the max number of trails from a category
    [-FF]: scrape the entire site. if this flag is passed all others will be ignored
    [-p]: Enter the number of photos to extract from Flickr API. Default 5
    """

import requests
from bs4 import BeautifulSoup as bs
from webfunctions import get_page
from trail_scraper import get_trail
import config as cfg
import sys
import db_handler
import credentials
from flickrAPI import Flickr
from argparser import ArgParser

# TODO: add logging
# TODO: add testing


def get_trail_categories():
    """
    extracts the categories names and urls from https://www.wikiloc.com/trails
    :return: dictionary {category: url}
    """
    root_path = 'https://www.wikiloc.com/trails'
    root_html_string = get_page(root_path)
    root_soup = bs(root_html_string.content, 'html.parser')
    activities_container = root_soup.find('section', class_='activities-list row')
    activities = activities_container.find_all('a')
    categories = [('all', '')]
    for i, activity in enumerate(activities):
        categories.append((activity.text[:-len(' trails')], activity['href']))

    return categories


def get_trails_urls(category, range_limits):
    """
    scans a category from the last uploaded trails back until reaching max_trails trails
    :param category: [tuple], 1st entry category name, 2nd entry url
    :param range_limits: [tuple] (from_trail, to_trail)
    :return: dict {trail_id : (trail_name, trail_url)}
    """
    # maximum number of trails per page (MAX_TRAILS_PER_PAGE) is determined by wikiloc (25)
    from_trail, to_trail = range_limits
    trails_url_dict = {}
    for i in range(max(0, from_trail), min(to_trail, cfg.MAX_TRAILS_IN_CATEGORY), cfg.MAX_TRAILS_PER_PAGE):
        trails_list_url = category[1] + f'&s=last&from={i}&to={min(i + cfg.MAX_TRAILS_PER_PAGE, to_trail)}'
        trails_list_html = get_page(trails_list_url)
        trail_list_soup = bs(trails_list_html.content, 'html.parser')
        trail_list_container = trail_list_soup.find('ul', class_='trail-list')
        for trail in trail_list_container.find_all('a', class_='trail-title'):
            trail_id = int(trail['href'].rsplit('-', 1)[1])
            trails_url_dict[trail_id] = (trail.text, trail['href'])
    return trails_url_dict


def main():
    # categories_list = get_trail_categories()  # get new categories list of names and urls from website

    ap = ArgParser()
    ap.get_args()
    if len(sys.argv) == 1:
        print(ap.format_help())
        sys.exit()

    cat_to_scrape, range_list = ap.parse_handler()

    extracted_trails_counter = 0
    if credentials.DB['password'] == '' and cfg.SAVE_TRAIL_DATA:
        credentials.DB['password'] = input(f'DB password for user {credentials.DB["username"]}: ')
    for cat_name, cat_url in cat_to_scrape:
        print(f'getting urls from category: {cat_name}')
        for i in range(range_list[0], range_list[1], cfg.BATCH_SIZE):
            trails_data = []
            try:
                trail_urls = get_trails_urls((cat_name, cat_url), (i, min(i+cfg.BATCH_SIZE, range_list[1])))
            except Exception as e:
                print(f"Reached the end of category '{cat_name}'")
                break

            existing_trail_ids = db_handler.check_trails_in_db(trail_urls.keys())
            if existing_trail_ids is not None and len(existing_trail_ids) > 0:
                extracted_wikiloc_ids,_ = zip(*existing_trail_ids)
            else:
                extracted_wikiloc_ids = []
            for trail_id in trail_urls.keys():
                if trail_id in extracted_wikiloc_ids and not cfg.UPDATE_TRAILS:
                    print(f'Skipping trail id {trail_id}, already in DB')
                    continue
                try:
                    url = trail_urls[trail_id][1]
                    trail_data = get_trail(url)
                    extracted_trails_counter += 1

                    # for now print data to screen
                    if cfg.PRINT_TRAIL_DATA:
                        print('\n'.join([f'{key} : {value}' for key, value in trail_data.items()]))
                        print('---------------------------------------------\n')

                    # save data
                    if cfg.SAVE_TRAIL_DATA:
                        trails_data.append(trail_data)
                    print(f'\nextracted so far: {extracted_trails_counter}, last extracted {trail_id}')
                except ValueError as ve:
                    print(f'Value error while processing trail {trail_id}-{trail_urls[trail_id][1]}')
                    print(ve)
                    print(f'skipping trail')
                except TimeoutError as te:
                    print(f'Timeout error while processing trail {trail_id}-{trail_urls[trail_id][1]}')
                    print(te)
                    if 'trail_timeouts' in vars():
                        trail_timeouts += 1
                        if trail_timeouts >= cfg.MAX_TIMEOUTS:
                            print('Maximum number of timeouts reached, check your internet connection and try again')
                            return
                    else:
                        trail_timeouts = 1
                except requests.HTTPError as e:
                    print(f'HTTP error while processing trail {trail_id}-{trail_urls[trail_id][1]}')
                    print(e)
                    if 'trail_http_errors' in vars():
                        trail_http_errors += 1
                        if trail_http_errors >= cfg.MAX_HTTP_ERRORS:
                            print('Maximum number of trail http errors reached, check the site and try again')
                            return
                    else:
                        trail_http_errors = 1
            if cfg.GET_TRAIL_PHOTOS and len(trails_data) > 0:
                flickr = Flickr()
                for trail_data in trails_data:
                    photo_urls = flickr.get_photos_url(lat=trail_data['start_lat'], lon=trail_data['start_lon'], no_of_photos=ap.args.p)
                    trail_data['photo_urls'] = photo_urls
                    print(f'extracted {len(photo_urls)} photos for trail {trail_data["id"]}')
            if cfg.SAVE_TRAIL_DATA and len(trails_data) > 0:
                inserted, inserted_details = db_handler.insert_into_db(trails_data)
                print(f'{inserted} committed to database')
                if inserted is not 0:
                    committed_wikiloc_ids, _ = zip(*inserted_details)
                    for trail_id in trail_urls.keys():
                        if trail_id not in committed_wikiloc_ids:
                            print(f'Trail {trail_id} was not committed to database, please check the log')
                else:
                    print(f'None committed to database')


def test():
    url = 'https://www.wikiloc.com/running-trails/tp-bhandup-44546156'
    trail_data = get_trail(url)
    db_handler.insert_into_db([trail_data])

if __name__ == '__main__':
    main()
    # test()
