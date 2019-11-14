from bs4 import BeautifulSoup as bs
from webfunctions import get_page
from helperfunctions import parse_range_list
from trail_scraper import get_trail
import argparse
import time

# TODO: handle exceptions
# TODO: add logging
# TODO: add testing
# TODO: improve documentation and commenting

MAX_TRAILS_PER_PAGE = 25
MAX_TRAILS_IN_CATEGORY = 10000
DEFAULT_CATEGORY_NAME = 'Hiking'
DEFAULT_TRAIL_RANGE = '0-100'
TIMEOUT = 60*3  # seconds
BATCH_SIZE = MAX_TRAILS_PER_PAGE



def get_trail_categories():
    """
    extracts the categories names and urls from https://www.wikiloc.com/trails
    :return: dictionary category:url
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
    :param category_tuple, 2nd entry url:
    :param range_limits tuple (from_trail, to_trail):

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


def get_parser(category_names):
    """
    an argument parser to parse arguments: -C category -c category number(s)
    :return:
    """

    parser = argparse.ArgumentParser(description='Wikiloc.com scraper')
    parser.add_argument('-c', '--cat_int', type=int, choices=range(0, len(category_names)+1),
                        metavar="category to scrape int", help=f"{{{'choose by number' + ' ; '.join(category_names)}}}")
    parser.add_argument('-C', '--cat_str', choices={tuple(name for name in category_names)},
                        metavar="category to scrape string", help=f"{{{'choose by name' + ' ; '.join(category_names)}}}")
    parser.add_argument('-r', type=str, help="comma separated ranges [0-10000]",
                        metavar='trails range')
    parser.add_argument('-FF', '--extract_all', help='This will extract all available trails category by category',
                        action='store_true')
    return parser


def main():
    # get all category names and urls:
    categories_list = get_trail_categories()
    category_names = [f"[{str(i)}] {cat[0]}" for i, cat in enumerate(categories_list)]
    # print('\n'.join(category_names))

    args = get_parser(category_names).parse_args()

    if args.extract_all:
        cat_to_scrape = list(range(1, len(categories_list)))
        range_list = (0, 10000)
    else:
        if args.cat_int:
            cat_to_scrape = [args.cat_int]
        elif args.cat_str:
            cat_to_scrape = [cat[0] for cat in categories_list].index(args.cat_str)
            if cat_to_scrape == -1:
                cat_to_scrape = [cat[0] for cat in categories_list].index('Hiking')
        else:
            cat_to_scrape = [cat[0] for cat in categories_list].index('Hiking')

        try:
            if args.r:
                range_list = parse_range_list(args.r)[0]
            else:
                range_list = parse_range_list(DEFAULT_TRAIL_RANGE)[0]
        except ValueError:
            print(ValueError)
            return

    # get the category tuples from indexes
    categories_to_scrape = [categories_list[cat] for cat in cat_to_scrape]

    extracted_trails_counter = 0
    start_time = time.time()
    try:
        for category in categories_to_scrape:
            print(f'getting urls from category: {category[0]}')

            for i in range(range_list[0], range_list[1], BATCH_SIZE):
                trail_urls = get_trails_urls(category, (i, i+BATCH_SIZE))
                for trail_id in trail_urls.keys():
                    url = trail_urls[trail_id][1]
                    # TODO: add try/except TimeoutError for get_trail()
                    trail_data = get_trail(url)
                    extracted_trails_counter += 1
                    # for now print data to screen
                    print('\n'.join([f'{key} : {value}' for key, value in trail_data.items()]))
                    print(f'\nextracted so far: {extracted_trails_counter}')
                    print('---------------------------------------------\n')
                    # TODO: here add where to save data
                    if (time.time() - start_time) > TIMEOUT:
                        raise TimeoutError
    except TimeoutError:
        print(f'Process timed out, extracted {extracted_trails_counter} trails')


if __name__ == '__main__':
    main()
