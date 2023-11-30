import argparse

from Database import Database


def help():
    # prints all commands
    print("todo: prints all cmd commands")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--login')
    parser.add_argument('--password')
    parser.add_argument('method')

    args, unknown = parser.parse_known_args()
    # print(f'UNKNOWN {unknown}')

    return args


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


def print_all_accounts():
    num_of_records = db.count_all_accounts()
    print(num_of_records)


if __name__ == '__main__':

    passed_args = get_args()
    db = get_database_object()

    try:
        method = (passed_args.method).replace("-", "_")
        result = globals()[method]()
        if result is not None:
            db = result

    except KeyError:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists. Try using the help method ("
              f"e.g. python main.py help)")

    current_user = validate_login_info(passed_args.login, passed_args.password)



