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
    """

import requests
from bs4 import BeautifulSoup as bs
from webfunctions import get_page
from trail_scraper import get_trail
import argparse
import config as cfg
import sys
import db_handler
import credentials
import time

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


def get_parser():
    """
    an argument parser to parse arguments: -C category -c category number(s)
    :return:
    """
    parser = argparse.ArgumentParser(description='Wikiloc.com scraper')

    parser.add_argument('-c', '--cat_int', type=int, choices=range(1, len(cfg.CATEGORIES)+2),
                        metavar="category to scrape int",
                        help="{{choose by number\n" +
                             "; ".join([str(i + 1) + ': ' + name for i, name in enumerate(cfg.CAT_NAMES)]) + '}}')
    parser.add_argument('-C', '--cat_str', type=str.lower, choices=cfg.CAT_NAMES,
                        metavar="category to scrape string",
                        help=f"{{{'choose by name' + ' ; '.join(cfg.CAT_NAMES)}}}")
    parser.add_argument('-r', type=str, help="range of trails to extract, dash separated e.g. '0-100'",
                        metavar='trails range')
    parser.add_argument('-f', help='This will extract all available trails from the chosen category',
                        action='store_true')
    parser.add_argument('-FF', '--extract_all', help='This will extract all available trails category by category',
                        action='store_true')
    # TODO: make country arg work
    # parser.add_argument('--country', metavar="country to scrape", help="choose by country name")

    return parser


def parse_handler(args):
    """ Function to handle the argument parser results
    :return: cat_to_scrape = list of category tuples of (name, url), range_list = tuple of range limits
    """
    if args.extract_all:
        cat_to_scrape = [(name, url) for name, url in cfg.CATEGORIES.values()]
        range_list = (0, cfg.MAX_TRAILS_IN_CATEGORY)
    else:
        if args.cat_int:
            cat_to_scrape = [cfg.CATEGORIES[args.cat_int]]
        elif args.cat_str:
            cat_indices = cfg.CAT_NAMES.index(args.cat_str) + 1
            cat_to_scrape = [cfg.CATEGORIES[cat_indices]]
        else:
            cat_to_scrape = [cfg.CATEGORIES[2]]  # Choose Hiking category by default

        try:
            if args.r:
                range_list = parse_range(args.r)
            elif args.f:
                range_list = (0, cfg.MAX_TRAILS_IN_CATEGORY)
            else:
                range_list = (0, cfg.DEFAULT_TRAIL_RANGE)
        except ValueError:
            print('Could not parse your requested range, please use numbers and dashes: e.g. "2-86" ')
            print(ValueError)
            return

    return cat_to_scrape, range_list


def parse_range(r):
    """ Function to parse range list string. e.g. "1-10" -> return tuple (0, 100)"""
    if not r:
        return []
    parts = r.split("-")
    if len(parts) == 1:  # if given 1 value, take range from 0->value
        return 0, int(r)
    elif len(parts) == 2:
        return int(parts[0]), int(parts[1])
    if len(parts) > 2:
        raise ValueError("Invalid range: {}".format(r))


def main():
    # categories_list = get_trail_categories()  # get new categories list of names and urls from website
    args = get_parser().parse_args()
    if len(sys.argv) == 1:
        print(get_parser().format_help())
        sys.exit()

    cat_to_scrape, range_list = parse_handler(args)

    extracted_trails_counter = 0
    if credentials.DB['password'] == '':
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
                    print(f'\nextracted so far: {extracted_trails_counter}')
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
                #TODO: add global timeout if needed (maybe debugging?)
            if cfg.GET_TRAIL_PHOTOS:
                for trail_data in trails_data:
                    flickr = Flickr()
                    trail_data['photo_urls'] = flickr.get_photo_urls(lat=trail_data['start_lat'],
                                                                     lon=trail_data['start_lon'])
            if cfg.SAVE_TRAIL_DATA and len(trails_data)> 0 :
                inserted, inserted_details = db_handler.insert_into_db(trails_data)
                print(f'{inserted} commited to database')
                committed_wikiloc_ids, _ = zip(*inserted_details)
                for trail_id in trail_urls.keys():
                    if trail_id not in committed_wikiloc_ids:
                        print(f'Trail {trail_id} was not committed to database, please check the log')


if __name__ == '__main__':
    main()
