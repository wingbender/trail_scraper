from bs4 import BeautifulSoup as bs
from trail_scraper import get_trail
from webfunctions import get_page
from helperfunctions import parse_range_list


MAX_TRAILS_PER_PAGE = 25
MAX_TRAILS_IN_CATEGORY = 10000


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


def get_trails_urls(category_url, from_trail=0, to_trail=50):
    """
    scans a category from the last uploaded trails back until reaching max_trails trails
    :param category_url:
    :param from_trail:
    :param to_trail:
    :return: dict {trail_id : (trail_name, trail_url)}
    """
    trails_dict = dict()

    # TODO: expand the function to extract multiple categories

    # maximum number of trails per page (MAX_TRAILS_PER_PAGE) is determined by wikiloc (25)
    for i in range(max(0, from_trail), min(to_trail,MAX_TRAILS_IN_CATEGORY), MAX_TRAILS_PER_PAGE):
        trails_list_url = category_url + f'&s=last&from={i}&to={min(i + MAX_TRAILS_PER_PAGE, to_trail)}'
        trails_list_html = get_page(trails_list_url)
        trail_list_soup = bs(trails_list_html.content, 'html.parser')
        trail_list_container = trail_list_soup.find('ul', class_='trail-list')
        for trail in trail_list_container.find_all('a', class_='trail-title'):
            trails_dict[int(trail['href'].rsplit('-', 1)[1])] = (trail.text, trail['href'])
    return trails_dict


def main():
    # get all category names and urls:
    categories_list = get_trail_categories()
    category_names = [f"[{str(i)}] {cat[0]}" for i, cat in enumerate(categories_list)]
    print('\n'.join(category_names))

    cat_to_scrape = input('Please select a category (number) to scrape: ')

    while not cat_to_scrape.isdigit() or int(cat_to_scrape) < 0:
        cat_to_scrape = input('Please select a category (number) to scrape: ')
    cat_to_scrape=int(cat_to_scrape)
    ## loop through a category to extract all the trails in it starting from the latest
    trails_to_scrape = ['empty']

    try:
        range_list = input("Please enter a range of trails to scrape "
                           "in comma separated ranges , max is 10000 are: ")
        range_list = parse_range_list(range_list)
    except ValueError:
        print(ValueError)
        return
    trails_dictionary = dict()
    for rng in range_list:
        trails_dictionary.update(get_trails_urls(categories_list[cat_to_scrape][1], from_trail=rng[0], to_trail=rng[1]))

    for i, trail_id in enumerate(trails_dictionary.keys()):
        print(f'trail #{i+1} of {len(trails_dictionary.keys())}: {trails_dictionary[trail_id][0]}')
        trails_dictionary[trail_id] = get_trail(trails_dictionary[trail_id][1])

    for trail_id in trails_dictionary.keys():
        # for tag in ['Time', 'Moving time', 'Uploaded', 'Recorded']:
        #     if tag in trails_dictionary[trail_id]:
        #         print(trails_dictionary[trail_id][tag][0])
        print(trails_dictionary[trail_id])

    # print(len(trails_dictionary.keys()))
    # print('\n'.join([f'{key} : {value[0]} - {value[1]}' for key, value in trails_dictionary.items()]))
    # print(get_trail_categories())
    # pass


def test():
    pass


if __name__ == '__main__':
    test()
    main()
