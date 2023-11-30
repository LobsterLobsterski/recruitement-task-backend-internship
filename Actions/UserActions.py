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



