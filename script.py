import argparse
import os
import sqlite3
from sqlite3 import Error

from Readers.CsvReader import CsvReader
from Readers.JsonReader import JsonReader
from Readers.XmlReader import XmlReader


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
    except Error as e:
        print(e)
    finally:
        create_table(conn)
        add_data_to_database(conn, datafile_paths)
        return conn


def create_table(conn):
    sql1 = """ CREATE TABLE IF NOT EXISTS user
                (
                  firstname text NOT NULL,
                  telephone_number text NOT NULL,
                  email text NOT NULL,
                  password text NOT NULL,
                  role text NOT NULL,
                  created_at text NOT NULL,
                  id INT NOT NULL,
                  PRIMARY KEY (id)
                );"""

    sql2 = """CREATE TABLE IF NOT EXISTS child
                (
                  id INT NOT NULL,
                  name text NOT NULL,
                  age INT NOT NULL,
                  parent_id INT NOT NULL,
                  PRIMARY KEY (id),
                  FOREIGN KEY (parent_id) REFERENCES user(id)
                );"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)
    except Error as e:
        print(f'Error while creating the database: {e}')


def read_datafiles(paths):
    data = []
    print(paths)
    for path in paths:
        # path = paths[0]
        reader = None

        if path[-3:] == "csv":
            reader = CsvReader(path)

        elif path[-4:] == "json":
            reader = JsonReader(path)

        elif path[-3:] == "xml":
            reader = XmlReader(path)

        data += reader.read()
        # break

    return data


def add_data_to_database(conn, paths):
    data = read_datafiles(paths)
    print(f"ALL DATA: {data}")

    # sql = """INSERT INTO Users(firstname, telephone_number, email, password, role, created_at, children) VALUES(?,
    #         ?,?,?,?,?,?) """
    #
    # try:
    #     cursor = conn.cursor()
    #     cursor.execute(sql)
    # except Error as e:
    #     print(e)


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

    try:
        globals()[passed_args.method]()
    except KeyError:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists. Try using the help method ("
              f"e.g. python main.py help)")
