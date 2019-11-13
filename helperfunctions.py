

def parse_range_list(rl):
    def parse_range(r):
        if len(r) == 0:
            return []
        parts = r.split("-")
        if len(parts) > 2:
            raise ValueError("Invalid range: {}".format(r))
        return int(parts[0]), int(parts[-1])
    a = []
    return list(map(parse_range, rl.split(',')))
    # for rng in list(map(parse_range, rl.split(','))):
    #     a = a+list(rng)
    # return sorted(set(a))


def test():
    print(parse_range_list('5-7,13,0-6'))
    assert parse_range_list('5-7,13,0-6') == [(5, 7), (13, 13), (0, 6)]
    assert parse_range_list('4-6') == [(4, 6)]
    assert parse_range_list('3') == [(3, 3)]


if __name__ == '__main__':
    test()
