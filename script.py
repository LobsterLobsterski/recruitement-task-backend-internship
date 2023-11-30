import argparse

from Database import Database


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--login')
    parser.add_argument('--password')
    parser.add_argument('method')

    args, unknown = parser.parse_known_args()
    # print(f'UNKNOWN {unknown}')

    return args


def help():
    # prints all commands
    print("todo: prints all cmd commands")


def print_all_accounts():
    num_of_records = db.count_all_accounts()
    if num_of_records == -1:
        print("\033[1mTry create_database method e.g. python script.py create_database ...\033[0m")
        return
    print(num_of_records)


def print_oldest_account():
    print(db.get_oldest_account())


def create_database():
    db = Database(r'data')
    db.create_database()
    db.test_database()

    return db


def get_database_object():
    return Database()


def validate_login_info(login, password):
    logged_in_user = db.find_user(login, password)
    return logged_in_user


if __name__ == '__main__':

    passed_args = get_args()
    db = None
    if Database.does_database_exists():
        db = get_database_object()
        current_user = validate_login_info(passed_args.login, passed_args.password)

    try:
        method = passed_args.method.replace("-", "_")
        if method != "create_database" and db is None:
            print("CREATE DATABASE FIRST using \033[1mcreate_database method e.g. python script.py create_database "
                  "...\033[0m")
            exit()

        result = globals()[method]()

    except KeyError:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists. Try using the help method ("
              f"e.g. python main.py help)")





