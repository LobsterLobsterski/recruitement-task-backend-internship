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
    sql1 = """ CREATE TABLE IF NOT EXISTS Users
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

    sql2 = """CREATE TABLE IF NOT EXISTS Children
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
    # print(f"ALL DATA: {data}")
    parent_id = 0
    child_id = 0

    for user in data:

        user_sql = f"INSERT INTO Users(firstname, telephone_number, email, password, role, created_at, id) " \
                    f"VALUES('{user.firstname}', '{user.telephone_number}', '{user.email}', '{user.password}', " \
                    f"'{user.role}', '{user.created_at}', {parent_id})"

        try:
            cursor = conn.cursor()
            cursor.execute(user_sql)
            conn.commit()

            for child in user.children:
                try:
                    child_sql = f"INSERT INTO Children(id, name, age, parent_id) " \
                                f"VALUES({child_id}, '{child.name}', {child.age}, {parent_id})"
                    cursor.execute(child_sql)
                    conn.commit()
                except Error as e:
                    print(f"Error while inserting child data: {user}\nError: {e}")
                child_id += 1

            cursor.close()
        except Error as e:
            print(f"Error while inserting user data: {user}\nError: {e}")

        parent_id += 1

    print("all data inserted")


def get_all_datafiles_paths(dir_path):
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            datafile_paths.append(dir_path+"\\"+path)
        else:
            get_all_datafiles_paths(os.path.join(dir_path, path))


def test_that_data_has_been_successfully_saved(conn):
    sql = """SELECT * from Users WHERE id=0
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        assert records[0] == ('Tanner', '604020303', 'lowerykimberly@example.net', '6mKY!nP^+y', 'admin', '2023-08-27 23:36:00', 0)
        cursor.close()
    except Error as e:
        print(f"Error while getting data: {e}")


if __name__ == '__main__':

    datafile_paths = []
    get_all_datafiles_paths(r'data')

    conn = create_database(datafile_paths)

    test_that_data_has_been_successfully_saved(conn)

    passed_args = get_args()

    try:
        globals()[passed_args.method]()
    except KeyError:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists. Try using the help method ("
              f"e.g. python main.py help)")

    conn.close()
