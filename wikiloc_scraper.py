from bs4 import BeautifulSoup as bs
from webfunctions import get_page
from helperfunctions import parse_range_list
from trail_scraper import get_trail
import argparse
import time


MAX_TRAILS_PER_PAGE = 25
MAX_TRAILS_IN_CATEGORY = 10000
DEFAULT_CATEGORY_NAME = 'Hiking'
DEFAULT_TRAIL_RANGE = '0-100'
TIMEOUT = 60*3  # seconds



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


def get_trails_urls(categories, ranges):
    """
    scans a category from the last uploaded trails back until reaching max_trails trails
    :param category_url:
    :param from_trail:
    :param to_trail:
    :return: dict {trail_id : (trail_name, trail_url)}
    """
    trails_dict = dict()

    # TODO: expand the function to extract multiple categories

    for category in categories:
        print(f'getting urls from category: {category[0]}')
        extracted_trails = 0
        for rng in ranges:
            from_trail = rng[0]
            to_trail = rng[1]
            # maximum number of trails per page (MAX_TRAILS_PER_PAGE) is determined by wikiloc (25)
            for i in range(max(0, from_trail), min(to_trail,MAX_TRAILS_IN_CATEGORY), MAX_TRAILS_PER_PAGE):
                trails_list_url = category[1] + f'&s=last&from={i}&to={min(i + MAX_TRAILS_PER_PAGE, to_trail)}'
                trails_list_html = get_page(trails_list_url)
                trail_list_soup = bs(trails_list_html.content, 'html.parser')
                trail_list_container = trail_list_soup.find('ul', class_='trail-list')
                for trail in trail_list_container.find_all('a', class_='trail-title'):
                    trail_id = int(trail['href'].rsplit('-', 1)[1])
                    trails_dict[trail_id] = (trail.text, trail['href'])
                    extracted_trails +=1
                    print(f'extracted {extracted_trails} from category {category[0]}')
    return trails_dict


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
        range_list = [(0, 10000)]
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
                range_list = parse_range_list(args.r)
            else:
                range_list = parse_range_list(DEFAULT_TRAIL_RANGE)
        except ValueError:
            print(ValueError)
            return

    trails_dictionary = get_trails_urls([categories_list[cat] for cat in cat_to_scrape], range_list)

    start_time = time.time()
    for i, trail_id in enumerate(trails_dictionary.keys()):
        print(f'trail #{i+1} of {len(trails_dictionary.keys())}: {trails_dictionary[trail_id][0]}')
        trail_data = get_trail(trails_dictionary[trail_id][1])

        trails_dictionary[trail_id] = trail_data
        print(trails_dictionary[trail_id])
        if (time.time() - start_time) > TIMEOUT:
            print(f'Timeout time of {TIMEOUT} seconds reached')
            break


    # for trail_id in trails_dictionary.keys():
    #     print(trails_dictionary[trail_id])


# def test():
#     pass


if __name__ == '__main__':
    # test()
    main()
