""" Function to parse range list that can be given as a command line argument to the main wikiloc_scraper.py file
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project """


def parse_range_list(rl):
    """
    parses a range string e.g. '2-100,230-500' to list of (from_item,to_item) tuples
    :param rl:
    :return: list of tuples of range limits
    """
    def parse_range(r):
        if not r:
            return []
        parts = r.split("-")
        if len(parts) == 1:  # if given 1 value, take range from 0->value
            return 0, r
        elif len(parts) == 2:
            return int(parts[0]), int(parts[-1])
        if len(parts) > 2:
            raise ValueError("Invalid range: {}".format(r))

    return list(map(parse_range, rl.split(',')))


def test():
    print(parse_range_list('5-7,13,0-6'))
    assert parse_range_list('5-7,13,0-6') == [(5, 7), (13, 13), (0, 6)]
    assert parse_range_list('4-6') == [(4, 6)]
    assert parse_range_list('3') == [(3, 3)]


if __name__ == '__main__':
    test()
