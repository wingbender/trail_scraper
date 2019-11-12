import re


MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
          'september': 9, 'october': 10, 'november': 11, 'december': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
          'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
          1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12
          }


def parse_time(time_string):

    time_string = time_string.replace('one', '1')
    if time_string.find('hour') is not -1 or time_string.find('minute') is not -1 or time_string.find('day') is not -1:
        total_time_minutes = 0
        # (regex, multiplier to minutes)
        for regex, multiplier in [(r"([\d]*) days", 24*60), (r"([\d]*) hour", 60), (r"([\d]*) minute", 1)]:
            match = re.search(regex, time_string)
            if match:
                total_time_minutes += int(match.groups()[0])*multiplier
        return total_time_minutes, 'minutes'
    else:
        date_string = 'YYYY-MM-DD'
        for part_symbol, regex in [('MM', r"([A-Z][a-z]*)"), ('DD', r"([0-9]{1,2}),"), ('YYYY', r"(20[0-9]{2})")]:
            match = re.search(regex,  time_string)
            if match:
                match_content = match.groups()[0]
                if match_content.isdigit():
                    date_string = date_string.replace(part_symbol, '{:02d}'.format(int(match_content)))
                else:
                    date_string = date_string.replace(part_symbol, str(MONTHS[match_content.lower()]))
        return date_string.replace('-DD', ''), 'YYYY-MM(-DD)'


def main():
    pass


def test():
    with open('time_strings', 'r') as time_file:
        time_strings = time_file.readlines()
    dt_list = []
    for dt_string in time_strings:

        print(dt_string)
        dt_list.append(parse_time(dt_string.strip()))
    results = zip(time_strings, dt_list)
    results = list(results)
    print(results)

    print('\n'.join([f"{time_string.strip()} : {output}" for (time_string, output) in results]))


if __name__ == '__main__':
    test()
    main()
