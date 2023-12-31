import os
import sqlite3
from sqlite3 import Error

from DatabaseTests import DatabaseTests
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
            self.get_all_datafiles_paths(r'data')
            self.create_database()
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

        return False

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

    def log_in(self, login, password):

        sql = f"SELECT * FROM Users WHERE password='{password}' AND (telephone_number='{login}' OR email='{login}')"

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()

        except Error as e:
            print(f"Error while finding user: {e}")
            return

        if len(records) == 1:
            children = self.get_children_by_parent_id(records[0][6])
            return User.from_array(records[0], children)

        elif len(records) == 0:
            print("Invalid Login")

        else:
            print("found many users with that info :(")

    def get_children_by_parent_id(self, parent_id):
        sql = f"SELECT name, age, id FROM Children WHERE parent_id={parent_id}"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()

        except Error as e:
            print(f"Error while finding children of user{parent_id}: {e}")
            return

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

    def find_similar_children_by_age(self, user_id):
        sql = f"""SELECT
                    u.firstname AS user_firstname,
                    u.telephone_number AS user_telephone_number,
                    u.email AS user_email,
                    u.password AS user_password,
                    u.role AS user_role,
                    u.created_at AS user_created_at,
                    u.id AS user_id
                FROM
                    Users u
                INNER JOIN
                    Children c ON u.id = c.parent_id
                WHERE
                    u.id <> {user_id}
                    AND EXISTS (
                        SELECT 1
                        FROM Children uc
                        WHERE uc.parent_id = u.id
                        AND ABS(uc.age - (SELECT age FROM Children WHERE parent_id = {user_id})) <= 1
                    )
                GROUP BY
                    u.id
                ORDER BY
                    u.firstname;
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            users = []

            for record in records:
                children = self.get_children_by_parent_id(record[6])
                users.append(User.from_array(record[:7], children))

            return users

        except Error as e:
            print(f"Error while counting user accounts data: {e}")

    def test_database(self):
        dt = DatabaseTests(self.conn, self)
        dt.run_all_tests()

    def close_connection(self):
        self.conn.close()
        self.conn = None

    def __establish_connection(self):
        try:
            self.conn = sqlite3.connect(r"database.sql")
        except Error as e:
            print(f"Error while connecting to the database: {e}")



