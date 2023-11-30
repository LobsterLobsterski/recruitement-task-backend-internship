import argparse

from Actions.AdminActions import AdminActions
from Actions.UserActions import UserActions
from Database import Database


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--login')
    parser.add_argument('--password')
    parser.add_argument('method')

    args, unknown = parser.parse_known_args()

    return args


def validate_login_info(login, password):
    logged_in_user = db.find_user(login, password)
    if logged_in_user is None:
        exit()
    return logged_in_user


if __name__ == '__main__':

    passed_args = get_args()
    db = None
    actionType = 'UserActions'
    current_user = None

    if Database.does_database_exists():
        db = Database()
        current_user = validate_login_info(passed_args.login, passed_args.password)

        if current_user.role == 'admin':
            actionType = 'AdminActions'

    try:
        method = passed_args.method.replace("-", "_")
        if method != "create_database" and db is None:
            print("CREATE DATABASE FIRST using \033[1mcreate_database method e.g. python script.py create_database "
                  "...\033[0m")
            exit()

        actionClass = globals()[actionType]
        getattr(actionClass, method)(db, current_user)

    except KeyError and AttributeError as e:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists or you don't have access to it."
              f"Try using the help method (e.g. python script.py help ...)")





