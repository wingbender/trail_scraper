""" entry point for wikiloc scraper to scrape trail data from wikiloc.com
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project

    The main function runs with command line arguments to scrape a range of files from a single category
    or loops through all the categories to scrape the entire site.

    command line arguments are:

    [-h] : show help message
    [-c category to scrape int]: category to scrape by number
    [-C category to scrape string]: category to scrape by name
    [-r trails range]: range of trails to scrape e.g.: '14-76'
    [-FF]: scrape the entire site. if this flag is passed all others will be ignored
    """

import requests
from bs4 import BeautifulSoup as bs
from webfunctions import get_page
from helperfunctions import parse_range_list
from trail_scraper import get_trail
import argparse
import time

# TODO: add logging
# TODO: add testing
# TODO: add to command line interface option to run nonstop on specific category
# TODO: transfer all the globals to config.py
MAX_TRAILS_PER_PAGE = 25  # This is determined by the wikiloc.com site, found out manually
MAX_TRAILS_IN_CATEGORY = 10000  # This is determined by the wikiloc.com site, found out manually
DEFAULT_CATEGORY_NAME = 'Hiking'  # Most interesting category for us right now, can be changed without any issue
DEFAULT_TRAIL_RANGE = '0-100'  # Taking the first 100 trails by default
# TIMEOUT = 60*3  # Timeout for the trail extraction operation
BATCH_SIZE = MAX_TRAILS_PER_PAGE  # The batch of URLs to extract before starting to extract each trail
MAX_TIMEOUTS = 30   # Max timeouts while extracting trails. if this number is reached,
                    # something is probably wrong and we should check it
MAX_HTTP_ERRORS = 5     # Max http errors while extracting trails. if this number is reached,
                           # something is probably wrong and we should check it


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
    :param category: [tuple], 2nd entry url
    :param range_limits: [tuple] (from_trail, to_trail)
    :return: dict {trail_id : (trail_name, trail_url)}
    """
    # maximum number of trails per page (MAX_TRAILS_PER_PAGE) is determined by wikiloc (25)
    from_trail, to_trail = range_limits
    trails_url_dict = {}
    for i in range(max(0, from_trail), min(to_trail, MAX_TRAILS_IN_CATEGORY), MAX_TRAILS_PER_PAGE):
        trails_list_url = category[1] + f'&s=last&from={i}&to={min(i + MAX_TRAILS_PER_PAGE, to_trail)}'
        trails_list_html = get_page(trails_list_url)
        trail_list_soup = bs(trails_list_html.content, 'html.parser')
        trail_list_container = trail_list_soup.find('ul', class_='trail-list')
        for trail in trail_list_container.find_all('a', class_='trail-title'):
            trail_id = int(trail['href'].rsplit('-', 1)[1])
            trails_url_dict[trail_id] = (trail.text, trail['href'])
    return trails_url_dict


def get_parser(categories_list):
    """
    an argument parser to parse arguments: -C category -c category number(s)
    :return:
    """
    category_names = [f"[{str(i)}] {cat[0]}" for i, cat in enumerate(categories_list)]

    # TODO: Make argument parser return help if no arguments are passed
    parser = argparse.ArgumentParser(description='Wikiloc.com scraper')
    parser.add_argument('-c', '--cat_int', type=int, choices=range(0, len(category_names)+1),
                        metavar="category to scrape int", help=f"{{{'choose by number' + ' ; '.join(category_names)}}}")
    parser.add_argument('-C', '--cat_str', choices={tuple(name for name in category_names)},
                        metavar="category to scrape string", help=f"{{{'choose by name' + ' ; '.join(category_names)}}}")
    parser.add_argument('--country', metavar="country to scrape", help="choose by country name")  # TODO: make country arg work
    parser.add_argument('-r', type=str, help="comma separated ranges [0-10000]",
                        metavar='trails range')
    parser.add_argument('-FF', '--extract_all', help='This will extract all available trails category by category',
                        action='store_true')
    return parser

def parse_handler(args):
    """ Function to handle the argument parser results """
    if args.extract_all:
        cat_to_scrape = CATEGORIES.keys()
        range_list = (0, 10000)
    else:
        if args.cat_int:
            cat_to_scrape = [args.cat_int]
        elif args.cat_str:
            cat_to_scrape = CATEGORIES[list(CATEGORIES.values()).index(args.cat_str)]
        else:
            cat_to_scrape = 2  # scrape HIKING category by default

        try:
            if args.r:
                range_list = parse_range_list(args.r)[0]
            else:
                range_list = parse_range_list(DEFAULT_TRAIL_RANGE)[0]
        except ValueError:
            print('Could not parse your requested range, please use numbers and dashes: "2-86" ')
            print(ValueError)
            return

def main():
    # TODO: simplify main, maybe implement classes

    # get all category names and urls:
    categories_list = get_trail_categories()
    args = get_parser(categories_list).parse_args()



    # get the category tuples from indexes
    try:
        categories_to_scrape = [categories_list[cat] for cat in cat_to_scrape]
    except requests.HTTPError:
        print('HTTP error while processing categories, exiting...')
        return

    except TimeoutError:
        print('Timeout error while processing categories, exiting...')
        return

    extracted_trails_counter = 0
    start_time = time.time()
    for category in categories_to_scrape:
        print(f'getting urls from category: {category[0]}')

        for i in range(range_list[0], range_list[1], BATCH_SIZE):
            trail_urls = get_trails_urls(category, (i, min(i+BATCH_SIZE, range_list[1])))
            for trail_id in trail_urls.keys():
                try:
                    url = trail_urls[trail_id][1]
                    # TODO: add try/except TimeoutError for get_trail()
                    trail_data = get_trail(url)
                    extracted_trails_counter += 1
                    # for now print data to screen
                    print('\n'.join([f'{key} : {value}' for key, value in trail_data.items()]))
                    print(f'\nextracted so far: {extracted_trails_counter}')
                    print('---------------------------------------------\n')
                    # TODO: here add where to save data

                except ValueError as ve:
                    print(f'Value error while processing trail {trail_id}-{trail_urls[trail_id][1]}')
                    print(ve)
                    print(f'skipping trail')

                except TimeoutError as te:
                    print(f'Value error while processing trail {trail_id}-{trail_urls[trail_id][1]}')
                    print(te)
                    if 'trail_timeouts' in vars():
                        trail_timeouts += 1
                        if trail_timeouts >= MAX_TIMEOUTS:
                            print('Maximum number of timeouts reached, check your internet connection and try again')
                            return
                    else:
                        trail_timeouts = 1
                except requests.HTTPError as e:
                    print(f'HTTP error while processing trail {trail_id}-{trail_urls[trail_id][1]}')
                    print(e)
                    if 'trail_http_errors' in vars():
                        trail_http_errors += 1
                        if trail_http_errors >= MAX_HTTP_ERRORS:
                            print('Maximum number of trail http errors reached, check the site and try again')
                            return
                    else:
                        trail_http_errors = 1
                #TODO: add global timeout if needed (maybe debugging?

                # if (time.time() - start_time) > TIMEOUT:
                #     print('Timed out while scraping the site. consider using a faster connection '
                #           'or extending the timeout limit')
                #     return


if __name__ == '__main__':
    main()
