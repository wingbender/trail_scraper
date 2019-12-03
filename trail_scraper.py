""" Functions to scrape trail data from a trail page in the website wikiloc.com
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project

    The main function get_trail() is called from wikiloc_scraper.py for a specific web page
    and returns trail_data dictionary """

from bs4 import BeautifulSoup as bs
from webfunctions import get_page
import re
import config as cfg


def get_trail(trail_page_url):
    """
    This function requests the web page, parses and extracts the trail data from the html, converts units and returns
    trail_data dictionary.
    :param trail_page_url:
    :return: dict trail_data
    """
    trail_page = get_page(trail_page_url)
    trail_data = extract_trail_data(trail_page)
    trail_data = convert_values(trail_data)
    return trail_data


def extract_trail_data(trail_page):
    """
    Extracts the trail details from an HTML string.
    returns trail_data dictionary where trail_data.keys() are the trail attributes and the values are
    tuples of numeric value and measurement units.
    :param trail_page (text)
    :return: trail_data (dictionary)
    """
    trail_id = int(str.rsplit(trail_page.url, '-', 1)[1])
    trail_soup = bs(trail_page.content, 'html.parser')
    trail_data = dict()
    trail_data['id'] = trail_id
    trail_data['title'] = trail_soup.find('h1').text.strip()
    trail_data['url'] = trail_page.url
    # user name and id
    user_id_container = trail_soup.find('a', attrs={"class": "user-image"})
    trail_data['user_name'] = user_id_container['title']
    trail_data['user_id'] = int(user_id_container['href'].split('=')[-1])
    title_container = trail_soup.find('h1')
    # country and trail category
    country_category_container = trail_soup.find('div', attrs={'class': "crumbs display"})
    trail_data['category'] = country_category_container.find("strong").text
    country = country_category_container.find("span")
    if country is not None:
        trail_data['country'] = country.text.split(' ')[-1]
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
    Function to parse trail data string into attributes, values and their units
    :param raw_data_string:
    :return:data tuple (attribute, value, units)
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
    """ Function takes trail_data dictionary, converts values to desired units and string formats, and returns
    new_data dictionary with the values and a separate units dictionary.
    :param trail_data dictionary
    :return new_data dictionary, units dictionary """
    new_data = {}
    # Division of attributes to different handling cases
    bool_attributes = ['Ends at start point (loop)']
    numeric_attributes = ['Distance', 'Elevation gain uphill', 'Elevation max',
                          'Elevation gain downhill', 'Elevation min']
    time_attributes = ['Time', 'Moving time']
    date_attributes = ['Uploaded', 'Recorded']
    id_attributes = ['id', 'title', 'category', 'country', 'user_name', 'user_id', 'url']

    for attribute, value in trail_data.items():

        if attribute in id_attributes:
            out_value = value

        elif attribute in bool_attributes:  # convert to bool True/False
            if value[0] == 'Yes':
                out_value = True
            else:
                out_value = False

        elif attribute in numeric_attributes:  # numerical values as floats and unit conversion
            out_value = float(value[0].replace(',', ''))
            if value[1] in cfg.CONVERSION_DICT.keys():
                out_value = out_value * cfg.CONVERSION_DICT[value[1]][0]
            elif value[1] not in ['m', 'km']:
                raise ValueError(f"Units of trail id {trail_data['id']} do not match the UNIT_MASTER key\n"
                                 f"Unit {value[1]} unrecognized!")
        elif attribute in time_attributes:
            total_time_minutes = 0
            # (regex, multiplier to minutes)
            for regex, multiplier in [(r"([\d]*) days", cfg.HOURS_IN_DAY * cfg.MINUTES_IN_HOUR),
                                      (r"([\d]*) hour", cfg.MINUTES_IN_HOUR),
                                      (r"([\d]*) minute", 1)]:
                match = re.search(regex, value[0].replace('one', '1'))
                if match:
                    total_time_minutes += int(match.groups()[0]) * multiplier
            out_value = total_time_minutes

        elif attribute in date_attributes:
            date_string = 'YYYY-MM-DD'
            for part_symbol, regex in [('MM', r"([A-Z][a-z]*)"), ('DD', r"([0-9]{1,2}),"), ('YYYY', r"(20[0-9]{2})")]:
                match = re.search(regex, value[0].replace('one', '1'))
                if match:
                    match_content = match.groups()[0]
                    if match_content.isdigit():
                        date_string = date_string.replace(part_symbol, '{:02d}'.format(int(match_content)))
                    else:
                        date_string = date_string.replace(part_symbol, str(cfg.MONTHS[match_content.lower()]))
            out_value = date_string.replace('-DD', '-01')  # if given only month, auto fill day as 1st

        else:
            continue

        new_data[attribute] = out_value

    # attributes outside of loop in order to change key name
    new_data['No of coordinates'] = int(trail_data['Coordinates'][0])
    new_data['Technical difficulty'] = trail_data['Technical difficulty:'][0]

    return new_data


def offline_data_test():
    """ Function to test data extraction from an offline web page already downloaded from wikiloc.com """
    # trail_path = 'https://www.wikiloc.com/hiking-trails/hexel-43199206'
    with open('Wikiloc_test_page.html', 'r', encoding='utf-8') as html_page:
        html_data = html_page.read()

    class MakeTestPage:
        """ Class to create a mock page for """
        def __init__(self, content, url):
            self.content = content
            self.url = url

    test_page = MakeTestPage(html_data, 'Wikiloc_test_page-43199206')  # added trail id to fake URL

    trail_data = extract_trail_data(test_page)
    trail_data = convert_values(trail_data)
    print('\n'.join([f'{key} : {value}' for key, value in trail_data.items()]))
    return trail_data


def online_data_test():
    """ Function to test online extraction of trail data from a trail page on wikiloc.com"""
    trail_data = get_trail("https://www.wikiloc.com/splitboard-trails/finsteraahorn-24124650")
    print('\n'.join([f'{key} : {value}' for key, value in trail_data.items()]))
    return trail_data
    # check if raises ValueError in get_trail() in case of units mismatch - changed UNITS_MASTER just for this


def main():
    offline_data_test()
    print()
    online_data_test()


if __name__ == '__main__':
    main()
