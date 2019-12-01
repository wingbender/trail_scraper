""" This file inputs new data into wikiloc scraper database
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project """

import pymysql
import config as cfg
import trail_scraper


def get_user_id(wikiloc_user_id,wikiloc_user_name, username=None, password=None):
    user_id = check_user_exists(wikiloc_user_id)
    if user_id is not -1:
        return user_id
    else:
        create_user(wikiloc_user_id,wikiloc_user_name)
        return check_user_exists(wikiloc_user_id)


def create_user(wikiloc_user_id, wikiloc_user_name, username=None, password=None):
    try:
        if not username:
            prompt = f'enter username: '
            username = input(prompt)
        if not password:
            prompt = f'enter password for user {username}:'
            password = input(prompt)
        host = 'localhost'
        connection = pymysql.connect(host='localhost',
                                     user=username,
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            command = f''' 
            INSERT INTO users(wikiloc_user_id, user_name)
            VALUES ('{wikiloc_user_id}', '{wikiloc_user_name}');
            '''
            res = cursor.execute(command)
        return res
    except Exception as e:
        print(f'Failed executing command: {command}\n Exception string:{e}')
    finally:
        connection.close()


def check_user_exists(wikiloc_user_id, username=None, password=None):
    try:
        if not username:
            prompt = f'enter username: '
            username = input(prompt)
        if not password:
            prompt = f'enter password for user {username}:'
            password = input(prompt)
        host = 'localhost'
        connection = pymysql.connect(host='localhost',
                                     user=username,
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            command = f''' 
            SELECT user_id
            FROM users
            WHERE wikiloc_user_id == '{wikiloc_user_id}';
            '''
            res = cursor.fetchone(command)
        return res
    except Exception as e:
        print(f'Failed executing command: {command}\n Exception string:{e}')
    finally:
        connection.close()


def insert_into_db(trails_data, username=None, password=None):
    """ Function that inserts "trail data" into trails, categories and users tables in database """
    try:
        if not username:
            prompt = f'enter username: '
            username = input(prompt)
        if not password:
            prompt = f'enter password for user {username}:'
            password = input(prompt)
        host = 'localhost'
        connection = pymysql.connect(host='localhost',
                                     user=username,
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            for trail_data in trails_data:
                # get the category id and user id:
                try:
                    category_id = cfg.CAT_NAMES.index(trail_data['category'].lower())
                except ValueError:
                    print(f"{trail_data['id']} category {trail_data['category']} does not match category list)")
                    category_id = None
                try:
                    user_id = get_user_id(trail_data['user_id'], trail_data['user_name'], username, password)
                except Exception as e:
                    print(f"Couldnot find user id = {trail_data['user_id']} or create new one in the databse")
                    print(f"exception message: {e}")
                command = f"""
                        INSERT INTO `trails`
                        ({', '.join(cfg.TRAIL_TO_DB_FIELDS_trails.values())},category_id, user_id) VALUES 
                        ({', '.join(["'" + str(trail_data[r]) + "'" for r in cfg.TRAIL_TO_DB_FIELDS_trails.keys() if r 
                                     in trail_data.keys()])}
                        ,{category_id},{user_id});"""
                # TODO: Handle missing 'moving time'.
                ###### WORKING STATEMENT:
                # INSERT INTO trails
                # (trail_id,wikiloc_id, title, url, country, distance, elevation_gain, elevation_max, elevation_loss, elevation_min, total_time, uploaded, recorded, n_coords, moving_time, difficulty,category_id, user_id)
                # VALUES
                # (8,24124650, 'Finsteraahorn', 'https://www.wikiloc.com/splitboard-trails/finsteraahorn-24124650', 'Switzerland', 11.58696, 1323.1368, 4198.0104, 1633.1184, 2625.8520000000003, 530, '2018-4-19', '2018-4-01', 2946, 345.2, 4,73,5);

                print(f'executing command: {command}')
                cursor.execute(command)
            connection.commit()
    except Exception as e:
        print(f'Failed executing command: {command}\n Exception string:{e}')
    finally:
        connection.close()


def main():
    trail_data = trail_scraper.get_trail("https://www.wikiloc.com/splitboard-trails/finsteraahorn-24124650")
    insert_into_db([trail_data], 'root', input('pass?: '))


if __name__ == '__main__':
    main()
