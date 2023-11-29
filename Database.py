import os
import sqlite3
from sqlite3 import Error

from Readers.CsvReader import CsvReader
from Readers.JsonReader import JsonReader
from Readers.XmlReader import XmlReader

class Database:
    datafile_paths = []
    conn=None

    def __init__(self, dir_path):
        self.get_all_datafiles_paths(dir_path)

    def get_all_datafiles_paths(self, dir_path):
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                self.datafile_paths.append(dir_path + "\\" + path)
            else:
                self.get_all_datafiles_paths(os.path.join(dir_path, path))

    def create_database(self):
        try:
            self.conn = sqlite3.connect(":memory:")
        except Error as e:
            print(f"Error while creating the database: {e}")
        finally:
            self.__create_tables()
            self.__add_data_to_database()

    def __create_tables(self):
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
            cursor = self.conn.cursor()
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.close()
        except Error as e:
            print(f'Error while creating the database: {e}')

    def __add_data_to_database(self):
        data = self.__read_datafiles()

        parent_id = 0
        child_id = 0

        for user in data:

            user_sql = f"INSERT INTO Users(firstname, telephone_number, email, password, role, created_at, id) " \
                       f"VALUES('{user.firstname}', '{user.telephone_number}', '{user.email}', '{user.password}', " \
                       f"'{user.role}', '{user.created_at}', {parent_id})"

            try:
                cursor = self.conn.cursor()
                cursor.execute(user_sql)
                self.conn.commit()

                for child in user.children:
                    try:
                        child_sql = f"INSERT INTO Children(id, name, age, parent_id) " \
                                    f"VALUES({child_id}, '{child.name}', {child.age}, {parent_id})"
                        cursor.execute(child_sql)
                        self.conn.commit()
                    except Error as e:
                        print(f"Error while inserting child data: {user}\nError: {e}")
                    child_id += 1

                cursor.close()
            except Error as e:
                print(f"Error while inserting user data: {user}\nError: {e}")

            parent_id += 1

        print("all data inserted")

    def __read_datafiles(self):
        data = []
        for path in self.datafile_paths:
            # path = paths[0]
            reader = None

            if path[-3:] == "csv":
                reader = CsvReader(path)

            elif path[-4:] == "json":
                reader = JsonReader(path)

            elif path[-3:] == "xml":
                reader = XmlReader(path)

            data += reader.read()

        return data

    def test_database(self):
        self.__test_that_data_has_been_successfully_saved()
    #     other tests

    def __test_that_data_has_been_successfully_saved(self):
        sql = """SELECT * from Users WHERE id=0
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()

            try:
                assert records[0] == ('Tanner', '604020303', 'lowerykimberly@example.net', '6mKY!nP^+y', 'admin',
                                      '2023-08-27 23:36:00', 0)
                print("\033[0;32m test_that_data_has_been_successfully_saved: SUCCESS \033[0m")
            except AssertionError as e:
                print("\033[0;31m test_that_data_has_been_successfully_saved: FAILURE \033[0m")
            finally:
                cursor.close()

        except Error as e:
            print(f"Error while getting data: {e}")

    def close_connection(self):
        self.conn.close()



