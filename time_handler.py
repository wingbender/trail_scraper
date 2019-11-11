import datetime
import re

months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
          'september': 9, 'october': 10, 'november': 11, 'december': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
          'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
          1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12
          }


def time_string_to_utc(time_string):
    time_regex = r" *(?P<hours>\w*) hours* (?P<minutes>\w*) minutes*"
    date_regex = r" *(?P<month>[\w]*) (?P<day>[0-9]*), (?P<year>[0-9]*)"
    time_string = time_string.replace('one', '1')

    # Try to fir the expression to time string
    match = re.match(time_regex, time_string)
    if match:
        # If time string format success, return time in seconds
        return match['hours']*360 + match['minutes']*60, 'seconds'
    else:
        # If the format is not time string, try as date string
        match = re.match(date_regex, time_string)
        # TODO: parse missing information dates (only month and year)
        if match:
            # if date string format is successful, return date object
            return datetime.date(int(match['year']), int(months[match['month'].lower()]), int(match['day'])), 'date'
    # if we couldn't parse as time or date, raise an exception
    raise ValueError(f'cant parse the string {time_string} as either time or date')



def main():
    pass


def test():
    time_strings = [['Moving time', ' one hour 46 minutes'], ['Time', ' 4 hours 16 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'],
                    ['Moving time', ' 2 hours 17 minutes'], ['Time', ' 3 hours 42 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'],
                    ['Moving time', ' 9 hours 3 minutes'], ['Time', ' 10 hours 31 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'], ['Time', ' 27 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'],
                    ['Moving time', ' one hour 24 minutes'], ['Time', ' one hour 31 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'],
                    ['Moving time', ' 5 hours 20 minutes'], ['Time', ' 6 hours 11 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'],
                    ['Moving time', ' 3 hours 58 minutes'], ['Time', ' 5 hours 37 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'],
                    ['Moving time', ' one hour 30 minutes'], ['Time', ' one hour 30 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'], ['Moving time', ' 13 minutes'],
                    ['Time', ' 13 minutes'], ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019'],
                    ['Moving time', ' one hour 43 minutes'], ['Time', ' 4 hours 44 minutes'],
                    ['Uploaded', 'November 11, 2019'], ['Recorded', 'November 2019']]
    dt_list = []
    for dt_string in time_strings:
        dt_list.append(time_string_to_utc(dt_string[1]))

    # {'id': 43457766, 'Distance': ('2.56', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('341', 'feet'), 'Elevation max': ('944', 'feet'),
    #  'Elevation gain downhill': ('341', 'feet'), 'Elevation min': ('666', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 47 minutes', None),
    #  'Time': (' one hour 9 minutes', None), 'Coordinates': ('609', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457764, 'Distance': ('5.86', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('1,394', 'feet'), 'Elevation max': ('952', 'feet'),
    #  'Elevation gain downhill': ('1,394', 'feet'), 'Elevation min': ('42', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Time': (' one hour 54 minutes', None), 'Coordinates': ('312', None),
    #  'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457753, 'Distance': ('6.38', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('46', 'feet'), 'Elevation max': ('127', 'feet'),
    #  'Elevation gain downhill': ('46', 'feet'), 'Elevation min': ('4', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 2 hours 8 minutes', None),
    #  'Time': (' 2 hours 16 minutes', None), 'Coordinates': ('1825', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457750, 'Distance': ('6.61', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('36', 'feet'), 'Elevation max': ('140', 'feet'),
    #  'Elevation gain downhill': ('36', 'feet'), 'Elevation min': ('74', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 2 hours 15 minutes', None),
    #  'Time': (' 2 hours 34 minutes', None), 'Coordinates': ('1870', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457744, 'Distance': ('1.66', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('509', 'feet'), 'Elevation max': ('1,144', 'feet'),
    #  'Elevation gain downhill': ('33', 'feet'), 'Elevation min': ('662', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Coordinates': ('40', None), 'Uploaded': ('November 11, 2019', None)}
    # {'id': 43457740, 'Distance': ('1.95', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('49', 'feet'), 'Elevation max': ('2,806', 'feet'),
    #  'Elevation gain downhill': ('49', 'feet'), 'Elevation min': ('2,763', 'feet'),
    #  'Technical difficulty:': ('Easy', None), 'Coordinates': ('79', None), 'Uploaded': ('November 11, 2019', None)}
    # {'id': 43457717, 'Distance': ('3.85', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('722', 'feet'), 'Elevation max': ('5,254', 'feet'),
    #  'Elevation gain downhill': ('722', 'feet'), 'Elevation min': ('4,564', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 28 minutes', None),
    #  'Time': (' 2 hours 27 minutes', None), 'Coordinates': ('1123', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457711, 'Distance': ('0.75', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('0', 'feet'), 'Elevation max': ('1,855', 'feet'),
    #  'Elevation gain downhill': ('23', 'feet'), 'Elevation min': ('1,823', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Time': (' 17 minutes', None), 'Coordinates': ('174', None),
    #  'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457698, 'Distance': ('3.57', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('722', 'feet'), 'Elevation max': ('1,024', 'feet'),
    #  'Elevation gain downhill': ('715', 'feet'), 'Elevation min': ('368', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 22 minutes', None),
    #  'Time': (' one hour 44 minutes', None), 'Coordinates': ('1015', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457678, 'Distance': ('5.32', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('66', 'feet'), 'Elevation max': ('57', 'feet'),
    #  'Elevation gain downhill': ('66', 'feet'), 'Elevation min': ('0', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 26 minutes', None),
    #  'Time': (' one hour 31 minutes', None), 'Coordinates': ('1455', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457663, 'Distance': ('14.54', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('6,942', 'feet'), 'Elevation max': ('4,030', 'feet'),
    #  'Elevation gain downhill': ('6,942', 'feet'), 'Elevation min': ('528', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 5 hours 10 minutes', None),
    #  'Time': (' 7 hours 44 minutes', None), 'Coordinates': ('3797', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457662, 'Distance': ('5.13', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('49', 'feet'), 'Elevation max': ('3,130', 'feet'),
    #  'Elevation gain downhill': ('95', 'feet'), 'Elevation min': ('3,010', 'feet'),
    #  'Technical difficulty:': ('Easy', None), 'Moving time': (' one hour 40 minutes', None),
    #  'Time': (' one hour 43 minutes', None), 'Coordinates': ('1505', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457657, 'Distance': ('4.43', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('108', 'feet'), 'Elevation max': ('518', 'feet'),
    #  'Elevation gain downhill': ('108', 'feet'), 'Elevation min': ('403', 'feet'),
    #  'Technical difficulty:': ('Easy', None), 'Coordinates': ('355', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457627, 'Distance': ('101.61', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('8,835', 'feet'), 'Elevation max': ('1,476', 'feet'),
    #  'Elevation gain downhill': ('8,835', 'feet'), 'Elevation min': ('-3', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Time': (' 10 hours 54 minutes', None),
    #  'Coordinates': ('11842', None), 'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457624, 'Distance': ('9.57', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('2,205', 'feet'), 'Elevation max': ('2,659', 'feet'),
    #  'Elevation gain downhill': ('4,744', 'feet'), 'Elevation min': ('17', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 3 hours 14 minutes', None),
    #  'Time': (' 5 hours 18 minutes', None), 'Coordinates': ('2598', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457608, 'Distance': ('9.66', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('16', 'feet'), 'Elevation max': ('318', 'feet'),
    #  'Elevation gain downhill': ('16', 'feet'), 'Elevation min': ('274', 'feet'),
    #  'Technical difficulty:': ('Difficult', None), 'Moving time': (' 3 hours 20 minutes', None),
    #  'Time': (' 3 hours 53 minutes', None), 'Coordinates': ('2710', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457596, 'Distance': ('3.09', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('272', 'feet'), 'Elevation max': ('1,612', 'feet'),
    #  'Elevation gain downhill': ('272', 'feet'), 'Elevation min': ('1,325', 'feet'),
    #  'Technical difficulty:': ('Easy', None), 'Moving time': (' one hour 20 minutes', None),
    #  'Time': (' one hour 53 minutes', None), 'Coordinates': ('898', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457578, 'Distance': ('2.93', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('118', 'feet'), 'Elevation max': ('1,487', 'feet'),
    #  'Elevation gain downhill': ('118', 'feet'), 'Elevation min': ('1,395', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 26 minutes', None),
    #  'Time': (' 2 hours 22 minutes', None), 'Coordinates': ('765', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457576, 'Distance': ('1.38', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('154', 'feet'), 'Elevation max': ('8,042', 'feet'),
    #  'Elevation gain downhill': ('85', 'feet'), 'Elevation min': ('7,898', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 26 minutes', None),
    #  'Time': (' one hour 17 minutes', None), 'Coordinates': ('104', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457557, 'Distance': ('8.85', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('1,598', 'feet'), 'Elevation max': ('12,537', 'feet'),
    #  'Elevation gain downhill': ('1,598', 'feet'), 'Elevation min': ('11,246', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Coordinates': ('1587', None),
    #  'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457534, 'Distance': ('8.24', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('2,116', 'feet'), 'Elevation max': ('3,586', 'feet'),
    #  'Elevation gain downhill': ('2,116', 'feet'), 'Elevation min': ('2,079', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 3 hours 16 minutes', None),
    #  'Time': (' 6 hours 57 minutes', None), 'Coordinates': ('2268', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457526, 'Distance': ('6.98', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('92', 'feet'), 'Elevation max': ('199', 'feet'),
    #  'Elevation gain downhill': ('102', 'feet'), 'Elevation min': ('105', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 43 minutes', None),
    #  'Time': (' one hour 8 minutes', None), 'Coordinates': ('597', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457510, 'Distance': ('4.36', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('509', 'feet'), 'Elevation max': ('163', 'feet'),
    #  'Elevation gain downhill': ('489', 'feet'), 'Elevation min': ('-4', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 2 hours 2 minutes', None),
    #  'Time': (' 2 hours 32 minutes', None), 'Coordinates': ('1268', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457506, 'Distance': ('4.54', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('223', 'feet'), 'Elevation max': ('2,237', 'feet'),
    #  'Elevation gain downhill': ('1,594', 'feet'), 'Elevation min': ('855', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 2 hours 21 minutes', None),
    #  'Time': (' 3 hours 26 minutes', None), 'Coordinates': ('1294', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457501, 'Distance': ('7.54', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('1,188', 'feet'), 'Elevation max': ('5,870', 'feet'),
    #  'Elevation gain downhill': ('1,188', 'feet'), 'Elevation min': ('5,384', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 42 minutes', None),
    #  'Time': (' one hour 46 minutes', None), 'Coordinates': ('1980', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457495, 'Distance': ('5.11', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('702', 'feet'), 'Elevation max': ('1,430', 'feet'),
    #  'Elevation gain downhill': ('702', 'feet'), 'Elevation min': ('737', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 30 minutes', None),
    #  'Time': (' one hour 33 minutes', None), 'Coordinates': ('1408', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457492, 'Distance': ('10.05', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('525', 'feet'), 'Elevation max': ('3,478', 'feet'),
    #  'Elevation gain downhill': ('702', 'feet'), 'Elevation min': ('2,933', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Coordinates': ('361', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457491, 'Distance': ('2.87', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('256', 'feet'), 'Elevation max': ('1,146', 'feet'),
    #  'Elevation gain downhill': ('256', 'feet'), 'Elevation min': ('969', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 57 minutes', None),
    #  'Time': (' one hour 10 minutes', None), 'Coordinates': ('759', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457490, 'Distance': ('0.43', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('3', 'feet'), 'Elevation max': ('525', 'feet'), 'Elevation gain downhill': ('3', 'feet'),
    #  'Elevation min': ('525', 'feet'), 'Technical difficulty:': ('Moderate', None), 'Time': (' 10 minutes', None),
    #  'Coordinates': ('128', None), 'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457489, 'Distance': ('5.5', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('922', 'feet'), 'Elevation max': ('991', 'feet'),
    #  'Elevation gain downhill': ('922', 'feet'), 'Elevation min': ('134', 'feet'),
    #  'Technical difficulty:': ('Easy', None), 'Time': (' 3 hours 5 minutes', None), 'Coordinates': ('1672', None),
    #  'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457488, 'Distance': ('0.18', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('3', 'feet'), 'Elevation max': ('3,038', 'feet'),
    #  'Elevation gain downhill': ('3', 'feet'), 'Elevation min': ('3,029', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 4 minutes', None), 'Time': (' 5 minutes', None),
    #  'Coordinates': ('52', None), 'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457487, 'Distance': ('2.43', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('92', 'feet'), 'Elevation max': ('3,218', 'feet'),
    #  'Elevation gain downhill': ('92', 'feet'), 'Elevation min': ('3,127', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Time': (' 48 minutes', None), 'Coordinates': ('2863', None),
    #  'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457486, 'Distance': ('5.57', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('213', 'feet'), 'Elevation max': ('1,615', 'feet'),
    #  'Elevation gain downhill': ('285', 'feet'), 'Elevation min': ('1,345', 'feet'),
    #  'Technical difficulty:': ('Easy', None), 'Moving time': (' one hour 39 minutes', None),
    #  'Time': (' one hour 47 minutes', None), 'Coordinates': ('1624', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457485, 'Distance': ('17.91', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('135', 'feet'), 'Elevation max': ('1,615', 'feet'),
    #  'Elevation gain downhill': ('1,558', 'feet'), 'Elevation min': ('104', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 4 hours 23 minutes', None),
    #  'Time': (' 5 hours 30 minutes', None), 'Coordinates': ('4074', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457483, 'Distance': ('0.09', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('10', 'feet'), 'Elevation max': ('1,937', 'feet'),
    #  'Elevation gain downhill': ('10', 'feet'), 'Elevation min': ('1,923', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Coordinates': ('25', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457437, 'Distance': ('3.99', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('440', 'feet'), 'Elevation max': ('434', 'feet'),
    #  'Elevation gain downhill': ('338', 'feet'), 'Elevation min': ('96', 'feet'),
    #  'Technical difficulty:': ('Easy', None), 'Moving time': (' one hour 18 minutes', None),
    #  'Time': (' 3 hours 22 minutes', None), 'Coordinates': ('935', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457436, 'Distance': ('3.58', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('1,033', 'feet'), 'Elevation max': ('1,113', 'feet'),
    #  'Elevation gain downhill': ('1,033', 'feet'), 'Elevation min': ('950', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 9 minutes', None),
    #  'Coordinates': ('833', None), 'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457434, 'Distance': ('11.87', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('1,460', 'feet'), 'Elevation max': ('1,537', 'feet'),
    #  'Elevation gain downhill': ('2,054', 'feet'), 'Elevation min': ('57', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 4 hours 12 minutes', None),
    #  'Time': (' 5 hours 27 minutes', None), 'Coordinates': ('3327', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457431, 'Distance': ('10.05', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('525', 'feet'), 'Elevation max': ('3,478', 'feet'),
    #  'Elevation gain downhill': ('702', 'feet'), 'Elevation min': ('2,933', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Coordinates': ('361', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457379, 'Distance': ('19.47', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('1,722', 'feet'), 'Elevation max': ('1,792', 'feet'),
    #  'Elevation gain downhill': ('2,231', 'feet'), 'Elevation min': ('1,018', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 2 hours 52 minutes', None),
    #  'Time': (' 9 hours 4 minutes', None), 'Coordinates': ('3264', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457375, 'Distance': ('3.6', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('1,280', 'feet'), 'Elevation max': ('2,435', 'feet'),
    #  'Elevation gain downhill': ('1,385', 'feet'), 'Elevation min': ('1,131', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 55 minutes', None),
    #  'Time': (' 3 hours 2 minutes', None), 'Coordinates': ('1037', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457373, 'Distance': ('5.56', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('535', 'feet'), 'Elevation max': ('617', 'feet'),
    #  'Elevation gain downhill': ('535', 'feet'), 'Elevation min': ('96', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 2 hours 30 minutes', None),
    #  'Time': (' 2 hours 53 minutes', None), 'Coordinates': ('1647', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457370, 'Distance': ('15.43', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('3,743', 'feet'), 'Elevation max': ('8,302', 'feet'),
    #  'Elevation gain downhill': ('3,005', 'feet'), 'Elevation min': ('5,662', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 4 hours 28 minutes', None),
    #  'Time': (' 6 hours 2 minutes', None), 'Coordinates': ('2759', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457363, 'Distance': ('9.33', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('725', 'feet'), 'Elevation max': ('3,210', 'feet'),
    #  'Elevation gain downhill': ('709', 'feet'), 'Elevation min': ('547', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 2 hours 53 minutes', None),
    #  'Time': (' 4 hours 18 minutes', None), 'Coordinates': ('2277', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457362, 'Distance': ('68.74', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('3,136', 'feet'), 'Elevation max': ('3,021', 'feet'),
    #  'Elevation gain downhill': ('5,499', 'feet'), 'Elevation min': ('63', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 54 minutes', None),
    #  'Time': (' 3 hours 39 minutes', None), 'Coordinates': ('5435', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457361, 'Distance': ('7.31', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('259', 'feet'), 'Elevation max': ('285', 'feet'),
    #  'Elevation gain downhill': ('259', 'feet'), 'Elevation min': ('92', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 2 hours 35 minutes', None),
    #  'Time': (' 2 hours 38 minutes', None), 'Coordinates': ('2146', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457360, 'Distance': ('4.55', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('108', 'feet'), 'Elevation max': ('80', 'feet'),
    #  'Elevation gain downhill': ('108', 'feet'), 'Elevation min': ('-5', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' one hour 25 minutes', None),
    #  'Time': (' one hour 37 minutes', None), 'Coordinates': ('995', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}
    # {'id': 43457359, 'Distance': ('2.7', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('3', 'feet'), 'Elevation max': ('1,916', 'feet'),
    #  'Elevation gain downhill': ('3', 'feet'), 'Elevation min': ('1,805', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 45 minutes', None), 'Time': (' 45 minutes', None),
    #  'Coordinates': ('756', None), 'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457357, 'Distance': ('1.12', 'miles'), 'Ends at start point (loop)': ('Yes', None),
    #  'Elevation gain uphill': ('43', 'feet'), 'Elevation max': ('927', 'feet'),
    #  'Elevation gain downhill': ('43', 'feet'), 'Elevation min': ('878', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 23 minutes', None), 'Time': (' 24 minutes', None),
    #  'Coordinates': ('316', None), 'Uploaded': ('November 11, 2019', None), 'Recorded': ('November 2019', None)}
    # {'id': 43457356, 'Distance': ('9.48', 'miles'), 'Ends at start point (loop)': ('No', None),
    #  'Elevation gain uphill': ('764', 'feet'), 'Elevation max': ('3,495', 'feet'),
    #  'Elevation gain downhill': ('745', 'feet'), 'Elevation min': ('3,172', 'feet'),
    #  'Technical difficulty:': ('Moderate', None), 'Moving time': (' 3 hours 32 minutes', None),
    #  'Time': (' 4 hours 18 minutes', None), 'Coordinates': ('5652', None), 'Uploaded': ('November 11, 2019', None),
    #  'Recorded': ('November 2019', None)}


if __name__ == '__main__':
    test()
    main()
