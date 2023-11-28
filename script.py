import argparse
import sqlite3
from sqlite3 import Error
import os
from dataclasses import dataclass


@dataclass
class Record:
    firstname: str
    telephone_number: str
    email: str
    password: str
    role: str
    created_at: str
    children: str

    def __init__(self, firstname, telephone_number, email, password, role, created_at, children=""):
        self.firstname = firstname
        self.telephone_number = telephone_number
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
        self.children = children

    def __repr__(self):
        return f"Record: (name:{self.firstname}, email:{self.email})"

    def to_array(self):
        return [self.firstname, self.telephone_number, self.email, self.password, self.role, self.created_at,
                self.children]


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
        add_data_to_database(conn, datafile_paths)
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


def get_all_data(paths):
    data = []
    for path in paths:
        print(path)
        # if path[-3:] == "csv":
        with open(path) as f:
            # lines = f.readlines()[1:]
            lines = f.read().split("\n")[1:]
            print(lines)
            for line in lines:
                split_line = line[:-1].split(";")
                # print(split_line)
                if len(split_line) == 6:
                    record = Record(split_line[0], split_line[1], split_line[2], split_line[3], split_line[4], split_line[5])
                else:
                    record = Record(split_line[0], split_line[1], split_line[2], split_line[3], split_line[4], split_line[5], split_line[6])

                # print(record)
                data.append(record)
            break

    return data


def add_data_to_database(conn, paths):
    data = get_all_data(paths)
    print(data)

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
    # print(f"passed args:{passed_args}")
    # print({'login': passed_args.login, 'password': passed_args.password})

    try:
        globals()[passed_args.method]()
    except KeyError:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists. Try using the help method ("
              f"e.g. python main.py help)")
