import requests
from bs4 import BeautifulSoup as bs


MAX_TRAILS_PER_PAGE = 25


# TODO: find trail location (long/lat or at least contry)
# TODO: get user id for each trail


def get_trail(trail_page_url):
    """
    extract the trail data from it's page
    :param trail_page_url:
    :return: dict trail_data
    """
    trail_page = get_page(trail_page_url)
    trail_id, trail_data = extract_trail_data(trail_page)
    return trail_id, trail_data


def get_headers():
    """
    generate headers to use when accessing a url
    # TODO implement random header generator
    :return:
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/77.0.3865.120 Safari/537.36'}
    return headers


def get_page(page_url):
    """
    returns an HTML string from page URL
    # TODO: add logging
    :param page_url:
    :return: string HTMLstring
    """
    try:
        page = requests.get(page_url, headers=get_headers())
        page.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return -1
    except Exception as err:
        print(f'Non HTTP error occurred: {err}')
        return -1
    if page.status_code == 200:
        return page
    else:
        return -1


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


def extract_trail_data(trail_html):
    """
    extracts the trail details from an HTML string.
    returns trail ID and trail_data dictionary where trail_data.keys() are the trail attributes and the values are
    tuples of numeric value and measurement units
    :param trail_html:
    :return:
    """
    # TODO: work better with bs
    trail_id = int(str.rsplit(trail_html.url, '-', 1)[1])
    trail_soup = bs(trail_html.content, 'html.parser')
    trail_data_container = trail_soup.find(id="trail-data")
    trail_data = dict()
    for hyperlink in trail_data_container.find_all('a', href=True, title=True):
        attribute, value, units = process_trail_data_string(hyperlink['title'])
        trail_data[attribute] = (value, units)
    for small_title in trail_data_container.find_all('h4'):
        attribute, value, units = process_trail_data_string(small_title.text)
        trail_data[attribute] = (value, units)
    return trail_id, trail_data


def process_trail_data_string(raw_data_string):
    """
    returns data tuple (attribute, value, units)
    :param raw_data_string:
    :return:
    """
    data_list = raw_data_string.split('\xa0')
    if len(data_list) == 2:
        # TODO: Handle time from words to numeric values
        attribute = data_list[0]
        value = data_list[1]
        units = 'None'
    if len(data_list) == 3:
        attribute = data_list[0]
        value = data_list[1]
        units = data_list[2]
    if len(data_list) == 4:
        attribute = data_list[0] + ' ' + data_list[1]
        value = data_list[2]
        units = data_list[3]
    return attribute, value, units


def test():
    trail_path = 'https://www.wikiloc.com/hiking-trails/hexel-43199206'
    trail_id, trail_data = get_trail(trail_path)
    print(trail_id)
    print('\n'.join([f'{key} : {value[0]} \t {value[1]}' for key, value in trail_data.items()]))


def main():
    ## get all category names and urls:
    categories_dictionary = get_trail_categories()
    category_names = list(categories_dictionary.keys())
    # print(category_names)

    ## loop through a category to extract all the trails in it starting from the latest

    trails_dictionary = get_trails_urls(categories_dictionary[category_names[0]], 50)
    # print(len(trails_dictionary.keys()))
    # print('\n'.join([f'{key} : {value[0]} - {value[1]}' for key, value in trails_dictionary.items()]))


if __name__ == '__main__':
    # test()
    main()
