from Actions.UserActions import UserActions


class AdminActions(UserActions):

    @staticmethod
    def print_all_accounts(*args):
        database = args[0]
        num_of_records = database.count_all_accounts()
        if num_of_records == -1:
            print("\033[1mTry create_database method e.g. python script.py create_database ...\033[0m")
            return
        print(num_of_records)

    @staticmethod
    def print_oldest_account(*args):
        database = args[0]
        print(database.get_oldest_account())

    @staticmethod
    def group_by_age(*args):
        database = args[0]
        for age, count in database.group_children_by_age():
            print(f"age: {age}, count: {count}")
