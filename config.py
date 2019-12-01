"""
    Global constants used through the program
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project
"""


MAX_TRAILS_PER_PAGE = 25  # This is determined by the wikiloc.com site, found out manually
MAX_TRAILS_IN_CATEGORY = 10000  # This is determined by the wikiloc.com site, found out manually
DEFAULT_CATEGORY_NAME = 'Hiking'  # Most interesting category for us right now, can be changed without any issue
DEFAULT_TRAIL_RANGE = 100  # Taking the first 100 trails by default
# TIMEOUT = 60*3  # Timeout for the trail extraction operation
BATCH_SIZE = MAX_TRAILS_PER_PAGE  # The batch of URLs to extract before starting to extract each trail
MAX_TIMEOUTS = 30  # Max timeouts while extracting trails. if this number is reached,
# something is probably wrong and we should check it
MAX_HTTP_ERRORS = 5  # Max http errors while extracting trails. if this number is reached,
# something is probably wrong and we should check it
PAGE_TIMEOUT = 5
MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
          'september': 9, 'october': 10, 'november': 11, 'december': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
          'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
          1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12}
CONVERSION_DICT = {'feet': [0.3048, 'm'], 'miles': [1.6093, 'km'], 'nm': [1.852, 'km']}
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
# List of the attributes extracted per trail and their units
UNITS_MASTER = {'id': None, 'title': None, 'url': None, 'user_name': None, 'user_id': None, 'category': None,
                'country': None, 'Distance': 'km', 'Ends at start point (loop)': 'bool', 'Elevation gain uphill': 'm',
                'Elevation max': 'm', 'Elevation gain downhill': 'm', 'Elevation min': 'm', 'Time': 'minutes',
                'Uploaded': 'YYYY-MM-DD', 'Recorded': 'YYYY-MM-DD', 'No of coordinates': None,
                'Moving time': 'minutes', 'Technical difficulty': None}

CATEGORIES = {1: ('mountain biking', 'https://www.wikiloc.com/trails/mountain-biking'),
              2: ('hiking', 'https://www.wikiloc.com/trails/hiking'),
              3: ('cycling', 'https://www.wikiloc.com/trails/cycling'),
              4: ('running', 'https://www.wikiloc.com/trails/running'),
              5: ('trail running ', 'https://www.wikiloc.com/trails/trail-running'),
              6: ('mountaineering', 'https://www.wikiloc.com/trails/mountaineering'),
              7: ('bicycle touring', 'https://www.wikiloc.com/trails/bicycle-touring'),
              8: ('walking', 'https://www.wikiloc.com/trails/walking'),
              9: ('motorcycling', 'https://www.wikiloc.com/trails/motorcycling'),
              10: ('ack country skiing', 'https://www.wikiloc.com/trails/back-country-skiing'),
              11: ('rail bike', 'https://www.wikiloc.com/trails/trail-bike'),
              12: ('atv', 'https://www.wikiloc.com/trails/atv'),
              13: ('kayaking - canoeing', 'https://www.wikiloc.com/trails/kayaking-canoeing'),
              14: ('sailing', 'https://www.wikiloc.com/trails/sailing'),
              15: ('snowshoeing', 'https://www.wikiloc.com/trails/snowshoeing'),
              16: ('cross country skiing', 'https://www.wikiloc.com/trails/cross-country-skiing'),
              17: ('alpine skiing', 'https://www.wikiloc.com/trails/alpine-skiing'),
              18: ('flying', 'https://www.wikiloc.com/trails/flying'),
              19: ('horseback riding', 'https://www.wikiloc.com/trails/horseback-riding'),
              20: ('dog sledging', 'https://www.wikiloc.com/trails/dog-sledging'),
              21: ('rock climbing', 'https://www.wikiloc.com/trails/rock-climbing'),
              22: ('inline skating', 'https://www.wikiloc.com/trails/inline-skating'),
              23: ('skating', 'https://www.wikiloc.com/trails/skating'),
              24: ('train', 'https://www.wikiloc.com/trails/train'),
              25: ('canyoneering', 'https://www.wikiloc.com/trails/canyoneering'),
              26: ('diving', 'https://www.wikiloc.com/trails/diving'),
              27: ('caving', 'https://www.wikiloc.com/trails/caving'),
              28: ('hang gliding', 'https://www.wikiloc.com/trails/hang-gliding'),
              29: ('ballooning', 'https://www.wikiloc.com/trails/ballooning'),
              30: ('snowboarding', 'https://www.wikiloc.com/trails/snowboarding'),
              31: ('ice climbing', 'https://www.wikiloc.com/trails/ice-climbing'),
              32: ('snowmobiling', 'https://www.wikiloc.com/trails/snowmobiling'),
              33: ('accessible', 'https://www.wikiloc.com/trails/accessible'),
              34: ('offroading', 'https://www.wikiloc.com/trails/offroading'),
              35: ('rowing', 'https://www.wikiloc.com/trails/rowing'),
              36: ('car', 'https://www.wikiloc.com/trails/car'),
              37: ('kiteboarding', 'https://www.wikiloc.com/trails/kiteboarding'),
              38: ('kite skiing', 'https://www.wikiloc.com/trails/kite-skiing'),
              39: ('sledge', 'https://www.wikiloc.com/trails/sledge'),
              40: ('kickbike', 'https://www.wikiloc.com/trails/kickbike'),
              41: ('paragliding', 'https://www.wikiloc.com/trails/paragliding'),
              42: ('for blind', 'https://www.wikiloc.com/trails/for-blind'),
              43: ('nordic walking', 'https://www.wikiloc.com/trails/nordic-walking'),
              44: ('motorcycle trials', 'https://www.wikiloc.com/trails/motorcycle-trials'),
              45: ('enduro', 'https://www.wikiloc.com/trails/enduro'),
              46: ('via ferrata', 'https://www.wikiloc.com/trails/via-ferrata'),
              47: ('swimming', 'https://www.wikiloc.com/trails/swimming'),
              48: ('orienteering', 'https://www.wikiloc.com/trails/orienteering'),
              49: ('multisport', 'https://www.wikiloc.com/trails/multisport'),
              50: ('stand up paddle (sup)', 'https://www.wikiloc.com/trails/stand-up-paddle-sup'),
              51: ('barefoot', 'https://www.wikiloc.com/trails/barefoot'),
              52: ('canicross', 'https://www.wikiloc.com/trails/canicross'),
              53: ('roller skiing', 'https://www.wikiloc.com/trails/roller-skiing'),
              54: ('longboarding', 'https://www.wikiloc.com/trails/longboarding'),
              55: ('mountain unicycling', 'https://www.wikiloc.com/trails/mountain-unicycling'),
              56: ('golf', 'https://www.wikiloc.com/trails/golf'),
              57: ('recreational vehicle', 'https://www.wikiloc.com/trails/recreational-vehicle'),
              58: ('airboat', 'https://www.wikiloc.com/trails/airboat'),
              59: ('segway', 'https://www.wikiloc.com/trails/segway'),
              60: ('camel', 'https://www.wikiloc.com/trails/camel'),
              61: ('freeride', 'https://www.wikiloc.com/trails/freeride'),
              62: ('unmanned aerial vehicle (uav)', 'https://www.wikiloc.com/trails/unmanned-aerial-vehicle-uav'),
              63: ('motorboat', 'https://www.wikiloc.com/trails/motorboat'),
              64: ('birdwatching - birding', 'https://www.wikiloc.com/trails/birdwatching-birding'),
              65: ('trailer bike', 'https://www.wikiloc.com/trails/trailer-bike'),
              66: ('water scooter (pwc)', 'https://www.wikiloc.com/trails/water-scooter-pwc'),
              67: ('handbike', 'https://www.wikiloc.com/trails/handbike'),
              68: ('rafting', 'https://www.wikiloc.com/trails/rafting'),
              69: ('downhill mountain biking (dh)', 'https://www.wikiloc.com/trails/downhill-mountain-biking-dh'),
              70: ('ebike', 'https://www.wikiloc.com/trails/ebike'),
              71: ('base jumping', 'https://www.wikiloc.com/trails/base-jumping'),
              72: ('joëlette', 'https://www.wikiloc.com/trails/joelette'),
              73: ('with baby carriage', 'https://www.wikiloc.com/trails/with-baby-carriage'),
              74: ('splitboard', 'https://www.wikiloc.com/trails/splitboard'),
              75: ('gravel Bike', 'https://www.wikiloc.com/trails/gravel-bike')}

CAT_NAMES = [name for name, url in CATEGORIES.values()]
DB_FILENAME = 'trails'

TRAIL_TO_DB_FIELDS_trails={
    'id': 'wikiloc_id',
    'title': 'title',
    'url': 'url',
    'user_id': 'user_id',
    'country': 'country',
    'Distance': 'distance',
    'Ends at start point (loop)': 'loop',
    'Elevation gain uphill': 'elevation_gain',
    'Elevation max': 'elevation_max',
    'Elevation gain downhill': 'elevation_loss',
    'Elevation min': 'elevation_min',
    'Time': 'total_time',
    'Uploaded': 'uploaded',
    'Recorded': 'recorded',
    'No of coordinates': 'n_coords',
    'Moving time': 'moving_time',
    'Technical difficulty': 'difficulty'}
