import requests
from bs4 import BeautifulSoup as bs
from webfunctions import get_page


# TODO: find trail location (long/lat or at least contry)
# TODO: get user id for each trail


def get_trail(trail_page_url):
    """
    extract the trail data from it's page
    :param trail_page_url:
    :return: dict trail_data
    """
    trail_page = get_page(trail_page_url)
    trail_data = extract_trail_data(trail_page)
    return trail_data


def extract_trail_data(trail_page):
    """
    extracts the trail details from an HTML string.
    returns trail_data dictionary where trail_data.keys() are the trail attributes and the values are
    tuples of numeric value and measurement units
    :param trail_page (text)
    :return: trail_data (dict)
    """
    # TODO: add to 'trail_data' dictionary: 1) trail category, 2) user_id/name 3) category
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


def convert_values(attribute, value, units):
    """ Function takes attribute, values and units and returns corrected entries:
     1. No / Yes -> bool True / False
     2. numerical values as floats
     3. datetime strings in *** format """
    if value == 'Yes' or value == 'No':  # No / Yes -> bool True / False
        out_units = 'bool'
        if value == 'Yes':
            out_value = True
        else:
            out_value = False
    elif value.count(' ') == 0 and units is not None:  # numerical values as floats
        out_value = float(value.replace(',', ''))
        if units == 'feet':
            out_value = out_value * 0.3048
            out_units = 'm'
        elif units == 'miles':
            out_value = out_value * 1.6093
            out_units = 'km'
    elif value.
    return out_value, out_units

def data_test():
    # trail_path = 'https://www.wikiloc.com/hiking-trails/hexel-43199206'
    # trail_id, trail_data = get_trail(trail_path)
    with open('Wikiloc_test_page.html', 'r', encoding='utf-8') as html_page:
        html_data = html_page.read()

    class MakeTestPage:
        """ Class to create a mock page for """
        def __init__(self, content, url):
            self.content = content
            self.url = url

    test_page = MakeTestPage(html_data, 'Wikiloc_test_page-1')

    trail_data = extract_trail_data(test_page)
    print('\n'.join([f'{key} : {value[0]} \t {value[1]}' for key, value in trail_data.items()]))


def main():

    data_test()


if __name__ == '__main__':
    main()
