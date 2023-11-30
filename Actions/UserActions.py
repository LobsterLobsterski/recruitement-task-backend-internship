class UserActions:

    @staticmethod
    def help(*args):
        # prints all commands
        print("todo: prints all cmd commands")

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








