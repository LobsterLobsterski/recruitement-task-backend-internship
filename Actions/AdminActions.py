from Actions.UserActions import UserActions


class AdminActions(UserActions):
    @staticmethod
    def help(*args):
        UserActions.help(args)
        print(f"""
        List of all admin exclusive commands:
            print-all-accounts          - displays all user accounts
            print-oldest-account        - displays the oldest account in the database
            group-by-age                - displays information about how many children of each age there are in the database
            """)

    @staticmethod
    def print_all_accounts(*args):
        database = args[0]
        num_of_records = database.count_all_accounts()
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
