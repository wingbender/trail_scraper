""" argument parser class for Wikiloc Scraper
authors: Roi Weinberger & Sagiv Yaari. Date: December 2019 """

import argparse
import config as cfg

class ArgParser(argparse.ArgumentParser):
    """ Class of argument parser functions. Child class of ArgumentParser from argparse module"""
    def __init__(self):
        super().__init__(description='Wikiloc.com scraper')

        self.add_argument('-r', type=str, help="range of trails to extract, dash separated e.g. '0-100'",
                            metavar='trails range')
        self.add_argument('-f', help='This will extract all available trails from the chosen category',
                            action='store_true')
        self.add_argument('-FF', '--extract_all', help='This will extract all available trails category by category',
                            action='store_true')
        self.add_argument('-p', metavar='no. of photos to extract', type=int, default=5,
                            help='Enter the number of photos to extract from Flickr API. Defaults to 5')
        self.add_argument('-c', '--cat_int', type=int, choices=range(1, len(cfg.CATEGORIES) + 2),
                            metavar="category to scrape int",
                            help="{{choose by number\n" +
                                 "; ".join([str(i + 1) + ': ' + name for i, name in enumerate(cfg.CAT_NAMES)]) + '}}')
        self.add_argument('-C', '--cat_str', type=str.lower, choices=cfg.CAT_NAMES,
                            metavar="category to scrape string",
                            help=f"{{{'choose by name' + ' ; '.join(cfg.CAT_NAMES)}}}")
        # TODO: make country arg work
        # self.add_argument('--country', metavar="country to scrape", help="choose by country name")
        self.args = []

    def get_args(self):
        """ Save arguments and parse them from the CLI """
        self.args = self.parse_args()

    def parse_handler(self):
        """ Function to handle the argument parser results """
        if self.args.extract_all:
            cat_to_scrape = [(name, url) for name, url in cfg.CATEGORIES.values()]
            range_list = (0, cfg.MAX_TRAILS_IN_CATEGORY)
        else:
            if self.args.cat_int:
                cat_to_scrape = [cfg.CATEGORIES[self.args.cat_int]]
            elif self.args.cat_str:
                cat_indices = cfg.CAT_NAMES.index(self.args.cat_str) + 1
                cat_to_scrape = [cfg.CATEGORIES[cat_indices]]
            else:
                cat_to_scrape = [cfg.CATEGORIES[2]]  # Choose Hiking category by default

            try:
                if self.args.r:
                    range_list = self.__parse_range(self.args.r)
                elif self.args.f:
                    range_list = (0, cfg.MAX_TRAILS_IN_CATEGORY)
                else:
                    range_list = (0, cfg.DEFAULT_TRAIL_RANGE)
            except ValueError:
                print('Could not parse your requested range, please use numbers and dashes: e.g. "2-86" ')
                print(ValueError)
                return

        return cat_to_scrape, range_list

    def __parse_range(self, r):
        """ Function to parse range list string. e.g. "1-10" -> return tuple (0, 100)"""
        if not r:
            return []
        parts = r.split("-")
        if len(parts) == 1:  # if given 1 value, take range from 0->value
            return 0, int(r)
        elif len(parts) == 2:
            return int(parts[0]), int(parts[1])
        if len(parts) > 2:
            raise ValueError("Invalid range: {}".format(r))