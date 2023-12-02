from sqlite3 import Error

from Dataclasses.User import User


class DatabaseTests:
    conn = None
    db = None

    def __init__(self, conn, db):
        self.conn = conn
        self.db = db

    def run_all_tests(self):
        self.__test_that_data_has_been_successfully_saved()
        self.__test_that_print_all_accounts_returns_correct_number_of_accounts()
        self.__test_that_print_oldest_account_returns_oldest_account()
        self.__test_that_group_by_age_returns_correctly_grouped_data()

    def __test_that_data_has_been_successfully_saved(self):
        sql = """SELECT * from Users WHERE id=0
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()

            assert records[0] == ('Tanner', '604020303', 'lowerykimberly@example.net', '6mKY!nP^+y', 'admin',
                                  '2023-08-27 23:36:00', 0)
            print("\033[0;32mtest_that_data_has_been_successfully_saved: SUCCESS\033[0m")

        except Error and AssertionError as e:
            print("\033[0;31mtest_that_data_has_been_successfully_saved: FAILURE")
            print(f"\tError while getting data: {e}\033[0m")

    def __test_that_print_all_accounts_returns_correct_number_of_accounts(self):
        try:
            assert self.db.count_all_accounts() == 91
            print("\033[0;32mtest_that_print_all_accounts_returns_correct_number_of_accounts: SUCCESS\033[0m")
        except AssertionError as e:
            print("\033[0;31mtest_that_print_all_accounts_returns_correct_number_of_accounts: FAILURE")
            print(f"\tError: {e}\033[0m")

    def __test_that_print_oldest_account_returns_oldest_account(self):
        try:
            assert self.db.get_oldest_account() == User("Justin", "678762794", "opoole@example.org", "password",
                                                        "admin", "2022-11-25 02:19:37", [])
            print("\033[0;32mtest_that_print_oldest_account_returns_oldest_account: SUCCESS\033[0m")
        except AssertionError as e:
            print("\033[0;31mtest_that_print_oldest_account_returns_oldest_account: FAILURE")
            print(f"\tError: {e}\033[0m")

    def __test_that_group_by_age_returns_correctly_grouped_data(self):
        try:
            assert self.db.group_children_by_age() == \
                   [(10, 4), (5, 5), (6, 5), (9, 5), (14, 5), (15, 5), (16, 5), (18, 5), (7, 6), (13, 7), (3, 8),
                    (4, 9), (8, 9), (12, 9), (2, 10), (17, 10), (11, 11), (1, 12)]

            print("\033[0;32mtest_that_group_by_age_returns_correctly_grouped_data: SUCCESS\033[0m")
        except AssertionError as e:
            print("\033[0;31mtest_that_group_by_age_returns_correctly_grouped_data: FAILURE")
            print(f"\tError: {e}\033[0m")


