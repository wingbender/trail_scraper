import requests
from bs4 import BeautifulSoup as bs


#TODO: find trail location (long/lat or at least contry)
#TODO: get user id for each trail

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
    #TODO implement random header generator
    :return:
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/77.0.3865.120 Safari/537.36'}
    return headers


def get_page(page_url):
    """
    returns an HTML string from page URL
    #TODO: add logging
    :param page_url:
    :return: string HTML string
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
    extracts the categories names and urls from main page
    :return:
    """
    #TODO: finish extraction of trail categories
    root_path = 'https://www.wikiloc.com/'
    root_HTML_string = get_page(root_path)
    root_soup = bs(root_HTML_string.content, 'html.parser')
    trail_categories_container = root_soup.find(id="trail-slider")
    categories = dict()
    for hyperlink in trail_categories_container.find_all('a', href=True, title=True):
         categories[hyperlink['title']] =  hyperlink['href']
    return categories


def get_trails_urls(**filters):
    # TODO: scan a category for it's trails and trail urls
    pass


def extract_trail_data(trail_page):
    """
    extracts the trail details from an HTML string.
    returns trail_data dictionary where trail_data.keys() are the trail attributes and the values are
    tuples of numeric value and measurement units
    :param trail_paeg (text):
    :return: trail_data (dict)
    """
    # TODO: work better with bs
    trail_id = int(str.rsplit(trail_page.url, '-', 1)[1])
    trail_soup = bs(trail_page.content, 'html.parser')
    trail_data_container = trail_soup.find(id="trail-data")
    trail_data = {'id': trail_id}
    for hyperlink in trail_data_container.find_all('a', href=True, title=True):
        attribute, value, units = process_trail_data_string(hyperlink['title'])
        trail_data[attribute] = (value, units)
    for small_title in trail_data_container.find_all('h4'):
        attribute, value, units = process_trail_data_string(small_title.text)
        trail_data[attribute] = (value, units)
    return trail_data


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
        units = None  # 'bool'
    elif len(data_list) >= 3:
        attribute = ' '.join(data_list[0:-2])
        value = data_list[-2]
        units = data_list[-1]
    return attribute, value, units

# def organize_data(attribute, value, units):
# 	"""  """

def data_test():
    # trail_path = 'https://www.wikiloc.com/hiking-trails/hexel-43199206'
    # trail_id, trail_data = get_trail(trail_path)
    with open('Wikiloc_test_page.html', 'r', encoding='utf-8') as html_page:
        html_data = html_page.read()

    class MakeTestPage:
        content = html_data
        url = 'Wikiloc_test_page-1'

    test_page = MakeTestPage()

    trail_data = extract_trail_data(test_page)
    print('\n'.join([f'{key} : {value[0]} \t {value[1]}' for key, value in trail_data.items()]))


def main():
    # print(get_trail_categories())
    # pass
    data_test()


if __name__ == '__main__':
    main()
