""" This file creates the databases and tables for wikiloc scraper data
    using the create_trails_db.sql script
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project """

import pymysql
import credentials

DB_CREATION_FILENAME = 'create_trails_db.sql'


def get_connection():
    if credentials.DB['password'] == '':
        credentials.DB['password'] = input(f'DB password for user {credentials.DB["username"]}: ')
    connection = pymysql.connect(host=credentials.DB['host'],
                                 user=credentials.DB['username'],
                                 password=credentials.DB['password'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor
                                 )
    return connection


def get_commands_file(filename):
    """
    This takes a sql script file and breaks it down to commands to be executed separately
    returns list(string) of individual commands
    """
    with open(filename, "r") as sql_file:
        # Split file in list
        ret = sql_file.read().split(';')
        # drop last empty entry
        ret.pop()
        return ret


def execute_commands(commands):
    """
    Executes all the commands in commands
    input: commands - list of sql commands to be executed
    """
    try:
        connection = get_connection()
        res = []
        with connection.cursor() as cursor:
            for command in commands:
                command += ';'
                print(f'executing command: {command}')
                cursor.execute(command)
                res.append(cursor.fetchall())
                connection.commit()
        return res
    except Exception as e:
        print(f'Failed executing command: {command}\n Exception string:{e}')
    finally:
        connection.close()


def main():
    commands = get_commands_file(DB_CREATION_FILENAME)
    results = execute_commands(commands)
    print([r for r in results if r])


if __name__ == '__main__':
    main()