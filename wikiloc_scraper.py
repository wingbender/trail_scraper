from bs4 import BeautifulSoup as bs
from trail_scraper import get_trail
from webfunctions import get_page


MAX_TRAILS_PER_PAGE = 25


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
    categories = dict()
    for activity in activities:
        categories[activity.text[:-len(' trails')]] = activity['href']
    return categories


def get_trails_urls(category_url, max_trails=50):
    """
    scans a category from the last uploaded trails back until reaching max_trails trails
    :param category_url:
    :param max_trails:
    :return: dict {trail_id : (trail_name, trail_url)}
    """
    trails_dict = dict()

    # maximum number of trails per page (MAX_TRAILS_PER_PAGE) is determined by wikiloc (25)
    for i in range(0, max_trails, MAX_TRAILS_PER_PAGE):
        trails_list_url = category_url + f'&s=last&from={i}&to={min(i+MAX_TRAILS_PER_PAGE , max_trails)}'
        trails_list_html = get_page(trails_list_url)
        trail_list_soup = bs(trails_list_html.content, 'html.parser')
        trail_list_container = trail_list_soup.find('ul', class_='trail-list')
        for trail in trail_list_container.find_all('a', class_='trail-title'):
            trails_dict[int(trail['href'].rsplit('-', 1)[1])] = (trail.text, trail['href'])
    return trails_dict


def main():
    ## get all category names and urls:
    categories_dictionary = get_trail_categories()
    category_names = list(categories_dictionary.keys())
    print(category_names)

    cat_to_scrape = input('Please select a category to scrape: ')

    while cat_to_scrape not in categories_dictionary.keys():
        cat_to_scrape = input('Please select a category to scrape')

    ## loop through a category to extract all the trails in it starting from the latest

    trails_to_scrape = None
    while type(trails_to_scrape) is not int:
        try:
            trails_to_scrape = int(input("Please enter number of trails to scrape [-1 for all]: "))
            if trails_to_scrape > 0:
                print(f'scraping {trails_to_scrape} trails from {cat_to_scrape}')
            elif trails_to_scrape == -1:
                print(f'scraping all trails from {cat_to_scrape}')
        except ValueError:
            print("%s is not an integer.\n" % trails_to_scrape)

    trails_dictionary = get_trails_urls(categories_dictionary[cat_to_scrape], trails_to_scrape)

    for i, trail_id in enumerate(trails_dictionary.keys()):
        print(f'trail #{i+1} of {trails_to_scrape}: {trails_dictionary[trail_id][0]}')
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
