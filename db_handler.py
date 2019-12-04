""" This file inputs new data into wikiloc scraper database
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project
"""

import pymysql
import config as cfg
import credentials
import trail_scraper


def get_connection():
    """
    Creates a connection to the DB based on the credentials in credentials.py
    and returns if for use
    """
    if credentials.DB['password'] == '':
        credentials.DB['password'] = input('pass?: ')
    connection = pymysql.connect(host=credentials.DB['host'],
                                 user=credentials.DB['username'],
                                 password=credentials.DB['password'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 db=credentials.DB['db'])
    return connection


def get_user_id(wikiloc_user_id, wikiloc_user_name):
    """
    If the user is known, returns the user_id from the database that corresponds to the wikiloc_user_id.
    If the user is new, creates a new user and returns its user_id
    """
    user_id = check_user_exists(wikiloc_user_id)
    if user_id is not None:
        return user_id['user_id']
    else:
        create_user(wikiloc_user_id, wikiloc_user_name)
        return check_user_exists(wikiloc_user_id)['user_id']


def create_user(wikiloc_user_id, wikiloc_user_name):
    """
    Creates a new user in the users table and returns its user_id
    """
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            command = f''' 
            INSERT INTO users(wikiloc_user_id, user_name)
            VALUES ('{wikiloc_user_id}', '{wikiloc_user_name}');
            '''
            res = cursor.execute(command)
            connection.commit()
        return res
    except Exception as e:
        print(f'Failed executing command: {command}\n Exception string:{e}')
    finally:
        connection.close()


def check_user_exists(wikiloc_user_id):
    """
    Checks if user exists based on its wikiloc_user_id and returns {'user_id':user_id}  if it does and None if not
    """
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            command = f'SELECT user_id FROM users WHERE wikiloc_user_id = {wikiloc_user_id};'
            cursor.execute(command)
            res = cursor.fetchone()
        return res
    except Exception as e:
        print(f'Failed executing command: {command}\n Exception string:{e}')
    finally:
        connection.close()


def build_insert_command(trail_data, category_id, user_id):
    """
    Creates an INSERT command based on the data given
    """
    # TODO: work on robustness, maybe create a dictionary first and then turn it into SQL command?
    command = ''
    command += 'INSERT INTO trails('
    command += ', '.join(
        [v for k, v in cfg.TRAIL_TO_DB_FIELDS_trails.items() if k in trail_data.keys() and v != 'user_id'])
    command += f',category_id, user_id) '
    command += '\nVALUES ('
    for dat in cfg.TRAIL_TO_DB_FIELDS_trails.keys():
        # Handling none existing fields (usually 'Moving time')
        if dat not in trail_data.keys():
            continue
        if dat == 'user_id':
            # TODO: maybe delete this attribute from the dictionary
            continue
        # Converting 'Technical difficulty' to INT for the database
        if dat.lower() == 'technical difficulty':
            command += str(cfg.DIFFICULTY_LEVELS[trail_data[dat]]) + ','
        # Handling strings (add '')
        elif type(trail_data[dat]) == str:
            command += f"'{pymysql.escape_string(trail_data[dat])}',"
        # Handling
        elif type(trail_data[dat]) in [int, float]:
            command += str(trail_data[dat]) + ','
        elif type(trail_data[dat]) == bool:
            command += str(1 if trail_data[dat] else 0) + ','
        else:
            raise ValueError
    command += f'{category_id}, {user_id});'
    return command


def insert_into_db(trails_data):
    """ Function that inserts "trail data" into trails, categories and users tables in database """
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f'USE trails')
            connection.commit()
            for trail_data in trails_data:
                # get the category id and user id:
                try:
                    category_id = cfg.CAT_NAMES.index(trail_data['category'].lower())
                except ValueError:
                    print(f"{trail_data['id']} category {trail_data['category']} does not match category list)")
                    category_id = None
                try:
                    user_id = get_user_id(trail_data['user_id'], trail_data['user_name'])
                except Exception as e:
                    print(f"Could not find user id = {trail_data['user_id']} or create new one in the database")
                    print(f"exception message: {e}")
                command = build_insert_command(trail_data, category_id, user_id)

                # print(f'executing command: {command}')
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f'Failed executing command: {command}\n Exception string:{e}')
            connection.commit()
    except Exception as e:
        print(f'Failed executing command: {command}\n Exception string:{e}')
    finally:
        connection.close()

    # TODO: implement updating if the trail already exists


def check_trails_in_db(trail_wikiloc_ids):
    """Returns a list of tuples with (database trail_id, wikiloc trail_id)"""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f'USE trails')
            connection.commit()
            command = r'SELECT trail_id, wikiloc_id FROM trails WHERE wikiloc_id in ('
            command += ','.join([str(m_trail_wikiloc_id) for m_trail_wikiloc_id  in trail_wikiloc_ids])
            command += ');'
            cursor.execute(command)
            result = cursor.fetchall()
    except Exception as e:
        print(f'Could not load existing trails from DB. \nException string: {e}')
    if result and result is not None:
        return [(item['wikiloc_id'], item['trail_id']) for item in result]
    else:
        return None



def main():
    pass


def test():
    # trail_url = 'https://www.wikiloc.com/trail-running-trails/porton-9-el-clasico-44046254'
    # trail_data = trail_scraper.get_trail(trail_url)
    # insert_into_db([trail_data])
    # trail_ids = get_trail_ids_from_db()
    #
    # print(trail_ids)
    res = check_trails_in_db([23098578,23096706,23068881,23068776,23061354,897])

if __name__ == '__main__':
    test()
    main()