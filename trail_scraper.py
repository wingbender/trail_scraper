import requests
from bs4 import BeautifulSoup as bs


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
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/77.0.3865.120 Safari/537.36'}
    return headers


def get_page(page_url):
    """
    returns an HTML string from page URL
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


def get_trails_urls(**filters):
    pass


def extract_trail_data(trail_html):
    """
    extracts the trail details from an HTML string.
    returns trail ID and trail_data dictionary where trail_data.keys() are the trail attributes and the values are
    tuples of numeric value and measurment units
    :param trail_html:
    :return:
    """
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
        attribute = data_list[0]
        value = data_list[1]
        units = 'None'
    if len(data_list) == 3:
        attribute = data_list[0]
        value = data_list[1]
        units = data_list[2]
    if len(data_list) == 4:
        attribute = data_list[0]+data_list[1]
        value = data_list[2]
        units = data_list[3]
    return attribute, value, units


def test():
    trail_path = 'https://www.wikiloc.com/hiking-trails/hexel-43199206'
    trail_id, trail_data = get_trail(trail_path)
    print(trail_id)
    print(trail_data)


def main():
    pass


if __name__ == '__main__':
    test()
    main()
