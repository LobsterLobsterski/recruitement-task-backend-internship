import argparse
import os
import sqlite3
from sqlite3 import Error


def help():
    # prints all commands
    print("todo")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--login')
    parser.add_argument('--password')
    parser.add_argument('method')

    args, unknown = parser.parse_known_args()
    # print(f'UNKNOWN {unknown}')

    return args


def create_database(datafile_paths):
    conn = None
    try:
        conn = sqlite3.connect(":memory:")
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        create_table(conn)
        # add_data_to_database(conn, datafile_paths)
        return conn


def create_table(conn):
    sql = """ CREATE TABLE IF NOT EXISTS Users (
                firstname text NOT NULL,
                telephone_number text PRIMARY KEY,
                email text NOT NULL,
                password text NOT NULL,
                role text NOT NULL,
                created_at text NOT NULL,
                children text
            ); """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except Error as e:
        print(f'Error while creating the database: {e}')


def get_all_datafiles_paths(dir_path):
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            datafile_paths.append(dir_path+"\\"+path)
        else:
            get_all_datafiles_paths(os.path.join(dir_path, path))


if __name__ == '__main__':

    datafile_paths = []
    get_all_datafiles_paths(r'data')
    print(datafile_paths)

    create_database(datafile_paths)

    passed_args = get_args()
    # print(f"passed args:{passed_args}")
    # print({'login': passed_args.login, 'password': passed_args.password})

    try:
        globals()[passed_args.method]()
    except KeyError:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists. Try using the help method ("
              f"e.g. python main.py help)")
