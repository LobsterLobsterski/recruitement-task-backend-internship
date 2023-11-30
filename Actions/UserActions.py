from Database import Database


class UserActions:
    @staticmethod
    def help(*args):
        print(f"""
        List of all user commands:
            print-children                  - displays data about your children
            find-similar-children-by-age    - displays the name, phone number and children of all users who have children of similar age to yours
            create-database                 - creates the database locally based on the data folder in the project directory
            test-database                   - runs various tests on the database
            help                            - displays all available commands
        """)

    @staticmethod
    def print_children(*args):
        user = args[1]
        for child in user.children:
            print(f"{child.name}, {child.age}")

    # make sure it works well
    @staticmethod
    def find_similar_children_by_age(*args):
        database = args[0]
        user = args[1]

        for record in database.find_similar_children_by_age(user):
            print(f"{record.firstname}, {record.telephone_number}: {[str(c.name)+', '+str(c.age) for c in record.children]}")

    @staticmethod
    def create_database(*args):
        if not Database.does_database_exists():
            Database(args)
        else:
            print("The Database already exists, try using help for a list of available commands")

    @staticmethod
    def test_database(*args):
        database = args[0]
        database.test_database(args)









