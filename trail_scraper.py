from bs4 import BeautifulSoup as bs
from webfunctions import get_page
import re

MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
          'september': 9, 'october': 10, 'november': 11, 'december': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
          'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
          1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12
          }
FEET_TO_METER = 0.3048
MILES_TO_KM = 1.6093
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60


def get_trail(trail_page_url):
    """
    extract the trail data from it's page
    :param trail_page_url:
    :return: dict trail_data
    """
    trail_page = get_page(trail_page_url)
    trail_data = extract_trail_data(trail_page)
    trail_data, units = convert_values(trail_data)
    return trail_data, units


def extract_trail_data(trail_page):
    """
    extracts the trail details from an HTML string.
    returns trail_data dictionary where trail_data.keys() are the trail attributes and the values are
    tuples of numeric value and measurement units
    :param trail_page (text)
    :return: trail_data (dict)
    """
    trail_id = int(str.rsplit(trail_page.url, '-', 1)[1])
    trail_soup = bs(trail_page.content, 'html.parser')
    trail_data = {}
    trail_data['id'] = trail_id
    trail_data['title'] = trail_soup.find('h1').text.strip()
    # user name and id
    user_id_container = trail_soup.find('a', attrs={"class": "user-image"})
    trail_data['user_name'] = user_id_container['title']
    trail_data['user_id'] = int(user_id_container['href'].split('=')[-1])
    title_container = trail_soup.find('h1')
    # country and trail category
    country_category_container = trail_soup.find('div', attrs={'class':"crumbs display"})
    trail_data['category'] = country_category_container.find("strong").text
    country = country_category_container.find("span")
    if country is not None:
        trail_data['country'] = country.text.split(' ')[-1]
    else:
        trail_data['country'] = 'Unknown'
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
    units_dict = {}
    bool_attributes = ['Ends at start point (loop)']
    numeric_attributes = ['Distance', 'Elevation gain uphill', 'Elevation max',
                          'Elevation gain downhill', 'Elevation min']
    time_attributes = ['Time', 'Moving time']
    date_attributes = ['Uploaded', 'Recorded']
    id_attributes = ['id', 'title', 'category', 'country', 'user_name', 'user_id']

    for attribute, value in trail_data.items():

        if attribute in id_attributes:
            out_value = value
            unit = None

        elif attribute in bool_attributes:  # convert to bool True/False
            if value[0] == 'Yes':
                out_value = True
            else:
                out_value = False
            unit = 'bool'

        elif attribute in numeric_attributes:  # numerical values as floats and unit conversion
            out_value = float(value[0].replace(',', ''))
            if value[1] == 'feet':
                out_value = out_value * 0.3048  # convert to meters
                unit = 'm'
            elif value[1] == 'miles':
                out_value = out_value * 1.6093  # convert to km
                unit = 'km'

        elif attribute in time_attributes:
            total_time_minutes = 0
            # (regex, multiplier to minutes)
            for regex, multiplier in [(r"([\d]*) days", HOURS_IN_DAY * MINUTES_IN_HOUR),
                                      (r"([\d]*) hour", MINUTES_IN_HOUR),
                                      (r"([\d]*) minute", 1)]:
                match = re.search(regex, value[0].replace('one', '1'))
                if match:
                    total_time_minutes += int(match.groups()[0]) * multiplier
            out_value = total_time_minutes
            unit = 'minutes'

        elif attribute in date_attributes:
            date_string = 'YYYY-MM-DD'
            for part_symbol, regex in [('MM', r"([A-Z][a-z]*)"), ('DD', r"([0-9]{1,2}),"), ('YYYY', r"(20[0-9]{2})")]:
                match = re.search(regex, value[0].replace('one', '1'))
                if match:
                    match_content = match.groups()[0]
                    if match_content.isdigit():
                        date_string = date_string.replace(part_symbol, '{:02d}'.format(int(match_content)))
                    else:
                        date_string = date_string.replace(part_symbol, str(MONTHS[match_content.lower()]))
            out_value = date_string.replace('-DD', '')
            unit = 'YYYY-MM(-DD)'

        else:
            continue

        new_data[attribute] = out_value
        units_dict[attribute] = unit

    # attributes outside of loop in order to change key name
    new_data['No of coordinates'] = int(trail_data['Coordinates'][0])
    units_dict['No of coordinates'] = None

    new_data['Technical difficulty'] = trail_data['Technical difficulty:'][0]
    units_dict['Technical difficulty'] = None

    return new_data, units_dict

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
    trail_data, units = convert_values(trail_data)
    print('\n'.join([f'{key} : {value} {units[key]},' for key, value in trail_data.items()]))


def main():
    data_test()


if __name__ == '__main__':
    main()
