import requests
from bs4 import BeautifulSoup as bs
from webfunctions import get_page
import re


# TODO: find trail location (long/lat or at least country)


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
    trail_data = {'id': [trail_id, None]}  # add 2nd item of None for unit field in dictionary. same for other unitless attributes
    # getting trail category from trail url
    trail_url_container = trail_soup.find('link', attrs={'rel': "canonical"})
    url = trail_url_container['href']
    trail_data['category'] = [re.search('.com/(\S+)-trails', url)[1], None]
    # user name and id
    user_id_container = trail_soup.find('a', attrs={"class": "user-image"})
    trail_data['user_name'] = [user_id_container['title'], None]
    trail_data['user_id'] = [int(user_id_container['href'].split('=')[-1]), None]
    # get trail data
    trail_data_container = trail_soup.find(id="trail-data")
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
        attribute = data_list[0]
        value = data_list[1]
        units = None
    elif len(data_list) >= 3:
        attribute = ' '.join(data_list[0:-2])
        value = data_list[-2]
        units = data_list[-1]
    return attribute, value, units


def convert_values(trail_data):
    """ Function takes trail_data dictionary and returns corrected entries:
     1. No / Yes -> bool True / False
     2. numerical values as floats
     3. datetime strings in *** format """
    new_data = {}
    bool_attributes = ['Ends at start point (loop)']
    numeric_attributes = ['Distance', 'Elevation gain uphill', 'Elevation max',
                         'Elevation gain downhill', 'Elevation min']
    time_attributes = ['Time', 'Uploaded', 'Recorded']
    id_attributes = ['id', 'category', 'user_name', 'user_id']

    for attribute, value in trail_data.items():
        out_value = ['', '']
        if attribute in id_attributes:
            out_value = value
        elif attribute in bool_attributes:
            if value[0] == 'Yes':
                out_value[0] = True
            else:
                out_value[0] = False
            out_value[1] = 'bool'
        elif attribute in numeric_attributes:  # numerical values as floats and unit conversion
            out_value[0] = float(value[0].replace(',', ''))
            if value[1] == 'feet':
                out_value[0] = out_value[0] * 0.3048
                out_value[1] = 'm'
            elif value[1] == 'miles':
                out_value[0] = out_value[0] * 1.6093
                out_value[1] = 'km'
        # elif attribute in time_attributes:
        # TODO: insert datetime conversion. need to think of correct format, numerical?
        else:
            continue
        new_data[attribute] = out_value
    # attributes outside of loop in order to change key name
    new_data['No of coordinates'] = [int(trail_data['Coordinates'][0]), None]
    new_data['Technical difficulty'] = list(trail_data['Technical difficulty:'])
    return new_data

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
    trail_data = convert_values(trail_data)
    print('\n'.join([f'{key} : {value[0]} \t {value[1]}' for key, value in trail_data.items()]))


def main():

    data_test()


if __name__ == '__main__':
    main()
