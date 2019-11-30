# import the mysql client for python

import pymysql.cursors
from getpass import getpass

DB_CREATION_FILENAME = 'create_trails_db.sql'


def get_commands_file(filename):
    with open(filename, "r") as sql_file:
        # Split file in list
        ret = sql_file.read().split(';')
        # drop last empty entry
        ret.pop()
        return ret


def execute_commands(commands, username=None, password=None):
    try:
        if not username:
            prompt = f'enter username: '
            username = input(prompt)
        if not password:
            prompt = f'enter password for user {username}:'
            password = input(prompt)
        host = 'localhost'
        # password = getpass(prompt=prompt)
        res=[]
        connection = pymysql.connect(host='localhost',
                                     user=username,
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            for command in commands:
                command +=';'
                print(f'executing command: {command}')
                cursor.execute(command)
                res.append(cursor.fetchall())
                connection.commit()
        return res
    except Exception as e:
        print(f'Failed executing command: {command}\n Exception string:{e}')
    finally:
        connection.close()


if __name__ == '__main__':
    password = input('pass for root: ')
    commands = get_commands_file(DB_CREATION_FILENAME)
    results = execute_commands(commands, 'root', password)
    print([r for r in results if r])




