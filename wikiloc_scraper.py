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
from trail_scraper import get_trail
import argparse
import config as cfg
import time

# TODO: add logging
# TODO: add testing
# TODO: add to command line interface option to run nonstop on specific category


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
    for i in range(max(0, from_trail), min(to_trail, cfg.MAX_TRAILS_IN_CATEGORY), cfg.MAX_TRAILS_PER_PAGE):
        trails_list_url = category[1] + f'&s=last&from={i}&to={min(i + cfg.MAX_TRAILS_PER_PAGE, to_trail)}'
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
    """ Function to handle the argument parser results
    :return: cat_to_scrape = list of category tuples of (name, url), range_list = tuple of range limits
    """
    if args.extract_all:
        cat_to_scrape = cfg.CATEGORIES.values()
        range_list = (0, 10000)
    else:
        if args.cat_int:
            cat_to_scrape = cfg.CATEGORIES[args.cat_int]
        elif args.cat_str:
            cat_indices = [name for name, url in cfg.CATEGORIES.values()].index(args.cat_str)
            cat_to_scrape = cfg.CATEGORIES[cat_indices]
        else:
            cat_to_scrape = cfg.CATEGORIES[2]  # scrape HIKING category by default

        try:
            if args.r:
                range_list = parse_range(args.r)
            else:
                range_list = parse_range(cfg.DEFAULT_TRAIL_RANGE)
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
    # TODO: simplify main, maybe implement classes

    # get all category names and urls:
    categories_list = get_trail_categories()
    args = get_parser(categories_list).parse_args()
    cat_to_scrape, range_list = parse_handler(args)


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
    for category in categories_to_scrape:
        print(f'getting urls from category: {category[0]}')
        for i in range(range_list[0], range_list[1], cfg.BATCH_SIZE):
            trail_urls = get_trails_urls(category, (i, min(i+cfg.BATCH_SIZE, range_list[1])))
            for trail_id in trail_urls.keys():
                try:
                    url = trail_urls[trail_id][1]
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


if __name__ == '__main__':
    # cats = get_trail_categories()
    # c = [f' {i} : (\'{c[0]}\',\'{c[1]}\')' for i, c in enumerate(cats)]
    # print(',\n'.join(c[1:]))

    main()
