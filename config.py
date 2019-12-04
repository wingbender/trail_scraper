"""
    Global constants used through the program
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project
"""

SAVE_TRAIL_DATA = True
PRINT_TRAIL_DATA = False
UPDATE_TRAILS = False

DB_FILENAME = 'trails'

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
CONVERSION_DICT = {'feet': [0.3048, 'm'], 'miles': [1.6093, 'km'], 'nm': [1.852, 'km'], 'nautical miles': [1.852, 'km']}
DIFFICULTY_LEVELS = {'Easy': 1, 'Moderate': 2, 'Difficult': 3, 'Very difficult': 4, 'Experts only': 5}
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
# List of the attributes extracted per trail and their units
UNITS_MASTER = {'id': None, 'title': None, 'url': None, 'user_name': None, 'user_id': None, 'category': None,
                'country': None, 'Distance': 'km', 'Ends at start point (loop)': 'bool', 'Elevation gain uphill': 'm',
                'Elevation max': 'm', 'Elevation gain downhill': 'm', 'Elevation min': 'm', 'Time': 'minutes',
                'Uploaded': 'YYYY-MM-DD', 'Recorded': 'YYYY-MM-DD', 'No of coordinates': None,
                'Moving time': 'minutes', 'Technical difficulty': None}

CATEGORIES = {0: ('mountain biking', 'https://www.wikiloc.com/trails/mountain-biking'),
              1: ('hiking', 'https://www.wikiloc.com/trails/hiking'),
              2: ('cycling', 'https://www.wikiloc.com/trails/cycling'),
              3: ('running', 'https://www.wikiloc.com/trails/running'),
              4: ('trail running ', 'https://www.wikiloc.com/trails/trail-running'),
              5: ('mountaineering', 'https://www.wikiloc.com/trails/mountaineering'),
              6: ('bicycle touring', 'https://www.wikiloc.com/trails/bicycle-touring'),
              7: ('walking', 'https://www.wikiloc.com/trails/walking'),
              8: ('motorcycling', 'https://www.wikiloc.com/trails/motorcycling'),
              9: ('ack country skiing', 'https://www.wikiloc.com/trails/back-country-skiing'),
              10: ('rail bike', 'https://www.wikiloc.com/trails/trail-bike'),
              11: ('atv', 'https://www.wikiloc.com/trails/atv'),
              12: ('kayaking - canoeing', 'https://www.wikiloc.com/trails/kayaking-canoeing'),
              13: ('sailing', 'https://www.wikiloc.com/trails/sailing'),
              14: ('snowshoeing', 'https://www.wikiloc.com/trails/snowshoeing'),
              15: ('cross country skiing', 'https://www.wikiloc.com/trails/cross-country-skiing'),
              16: ('alpine skiing', 'https://www.wikiloc.com/trails/alpine-skiing'),
              17: ('flying', 'https://www.wikiloc.com/trails/flying'),
              18: ('horseback riding', 'https://www.wikiloc.com/trails/horseback-riding'),
              19: ('dog sledging', 'https://www.wikiloc.com/trails/dog-sledging'),
              20: ('rock climbing', 'https://www.wikiloc.com/trails/rock-climbing'),
              21: ('inline skating', 'https://www.wikiloc.com/trails/inline-skating'),
              22: ('skating', 'https://www.wikiloc.com/trails/skating'),
              23: ('train', 'https://www.wikiloc.com/trails/train'),
              24: ('canyoneering', 'https://www.wikiloc.com/trails/canyoneering'),
              25: ('diving', 'https://www.wikiloc.com/trails/diving'),
              26: ('caving', 'https://www.wikiloc.com/trails/caving'),
              27: ('hang gliding', 'https://www.wikiloc.com/trails/hang-gliding'),
              28: ('ballooning', 'https://www.wikiloc.com/trails/ballooning'),
              29: ('snowboarding', 'https://www.wikiloc.com/trails/snowboarding'),
              30: ('ice climbing', 'https://www.wikiloc.com/trails/ice-climbing'),
              31: ('snowmobiling', 'https://www.wikiloc.com/trails/snowmobiling'),
              32: ('accessible', 'https://www.wikiloc.com/trails/accessible'),
              33: ('offroading', 'https://www.wikiloc.com/trails/offroading'),
              34: ('rowing', 'https://www.wikiloc.com/trails/rowing'),
              35: ('car', 'https://www.wikiloc.com/trails/car'),
              36: ('kiteboarding', 'https://www.wikiloc.com/trails/kiteboarding'),
              37: ('kite skiing', 'https://www.wikiloc.com/trails/kite-skiing'),
              38: ('sledge', 'https://www.wikiloc.com/trails/sledge'),
              39: ('kickbike', 'https://www.wikiloc.com/trails/kickbike'),
              40: ('paragliding', 'https://www.wikiloc.com/trails/paragliding'),
              41: ('for blind', 'https://www.wikiloc.com/trails/for-blind'),
              42: ('nordic walking', 'https://www.wikiloc.com/trails/nordic-walking'),
              43: ('motorcycle trials', 'https://www.wikiloc.com/trails/motorcycle-trials'),
              44: ('enduro', 'https://www.wikiloc.com/trails/enduro'),
              45: ('via ferrata', 'https://www.wikiloc.com/trails/via-ferrata'),
              46: ('swimming', 'https://www.wikiloc.com/trails/swimming'),
              47: ('orienteering', 'https://www.wikiloc.com/trails/orienteering'),
              48: ('multisport', 'https://www.wikiloc.com/trails/multisport'),
              49: ('stand up paddle (sup)', 'https://www.wikiloc.com/trails/stand-up-paddle-sup'),
              50: ('barefoot', 'https://www.wikiloc.com/trails/barefoot'),
              51: ('canicross', 'https://www.wikiloc.com/trails/canicross'),
              52: ('roller skiing', 'https://www.wikiloc.com/trails/roller-skiing'),
              53: ('longboarding', 'https://www.wikiloc.com/trails/longboarding'),
              54: ('mountain unicycling', 'https://www.wikiloc.com/trails/mountain-unicycling'),
              55: ('golf', 'https://www.wikiloc.com/trails/golf'),
              56: ('recreational vehicle', 'https://www.wikiloc.com/trails/recreational-vehicle'),
              57: ('airboat', 'https://www.wikiloc.com/trails/airboat'),
              58: ('segway', 'https://www.wikiloc.com/trails/segway'),
              59: ('camel', 'https://www.wikiloc.com/trails/camel'),
              60: ('freeride', 'https://www.wikiloc.com/trails/freeride'),
              61: ('unmanned aerial vehicle (uav)', 'https://www.wikiloc.com/trails/unmanned-aerial-vehicle-uav'),
              62: ('motorboat', 'https://www.wikiloc.com/trails/motorboat'),
              63: ('birdwatching - birding', 'https://www.wikiloc.com/trails/birdwatching-birding'),
              64: ('trailer bike', 'https://www.wikiloc.com/trails/trailer-bike'),
              65: ('water scooter (pwc)', 'https://www.wikiloc.com/trails/water-scooter-pwc'),
              66: ('handbike', 'https://www.wikiloc.com/trails/handbike'),
              67: ('rafting', 'https://www.wikiloc.com/trails/rafting'),
              68: ('downhill mountain biking (dh)', 'https://www.wikiloc.com/trails/downhill-mountain-biking-dh'),
              69: ('ebike', 'https://www.wikiloc.com/trails/ebike'),
              70: ('base jumping', 'https://www.wikiloc.com/trails/base-jumping'),
              71: ('joëlette', 'https://www.wikiloc.com/trails/joelette'),
              72: ('with baby carriage', 'https://www.wikiloc.com/trails/with-baby-carriage'),
              73: ('splitboard', 'https://www.wikiloc.com/trails/splitboard'),
              74: ('gravel Bike', 'https://www.wikiloc.com/trails/gravel-bike')}

CAT_NAMES = [name for name, url in CATEGORIES.values()]

TRAIL_TO_DB_FIELDS_trails={
    'id': 'wikiloc_id',
    'title': 'title',
    'url': 'url',
    'user_id': 'user_id',
    'country': 'country',
    'Distance': 'distance',
    'Ends at start point (loop)': 'is_loop',
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
