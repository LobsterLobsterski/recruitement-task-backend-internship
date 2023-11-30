import os
import sqlite3
from sqlite3 import Error

from Dataclasses.Child import Child
from Dataclasses.User import User
from Readers.CsvReader import CsvReader
from Readers.JsonReader import JsonReader
from Readers.XmlReader import XmlReader


class Database:
    datafile_paths = []
    conn = None

    def __init__(self, *args):
        if len(args) != 0:
            self.get_all_datafiles_paths(args[0])
        else:
            if self.does_database_exists():
                self.__establish_connection()

    def get_all_datafiles_paths(self, dir_path):
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                self.datafile_paths.append(dir_path + "\\" + path)
            else:
                self.get_all_datafiles_paths(os.path.join(dir_path, path))

    @staticmethod
    def does_database_exists():
        for path in os.listdir(r"C:\Users\tomas\Desktop\recruitement-task-backend-internship"):
            if path == "database.sql":
                return True

    def create_database(self):
        if self.does_database_exists():
            self.__establish_connection()
            return self

        open("database.sql", "x")

        try:
            self.conn = sqlite3.connect(r"database.sql")
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
                      FOREIGN KEY (parent_id) REFERENCES Users(id)
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

    def find_user(self, login, password):

        sql = f"SELECT * FROM Users WHERE password='{password}' AND (telephone_number='{login}' OR email='{login}')"

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()

        except Error as e:
            print(f"Error while finding user: {e}")
            return -1

        if len(records) == 1:
            children = self.get_children_by_parent_id(records[0][6])
            return User.from_array(records[0], children)

        elif len(records) == 0:
            print("Invalid Login")
            return -1
        else:
            print("found many users with that info :(")
            return -1

    def get_children_by_parent_id(self, parent_id):
        sql = f"SELECT name, age, id FROM Children WHERE parent_id={parent_id}"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()

        except Error as e:
            print(f"Error while finding children of user{parent_id}: {e}")
            return -1

        children = []
        for child_array in records:
            children.append(Child.from_array(child_array))

        return children

    def count_all_accounts(self):
        sql = """SELECT count(*) from Users"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            return records[0][0]

        except Error as e:
            print(f"Error while counting user accounts data: {e}")

        return -1

    def get_oldest_account(self):
        sql = """SELECT * from Users ORDER BY created_at ASC LIMIT 1"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            children = self.get_children_by_parent_id(records[0][6])
            return User.from_array(records[0], children)

        except Error as e:
            print(f"Error while counting user accounts data: {e}")

        return -1

    def group_children_by_age(self):
        sql = """SELECT age, COUNT(*) AS count_of_children
                 FROM Children
                 GROUP BY age
                 ORDER BY count_of_children;
              """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            return records

        except Error as e:
            print(f"Error while counting user accounts data: {e}")

        return -1

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

    def __establish_connection(self):
        try:
            self.conn = sqlite3.connect(r"database.sql")
        except Error as e:
            print(f"Error while connecting to the database: {e}")



