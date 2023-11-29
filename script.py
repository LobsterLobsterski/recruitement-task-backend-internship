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


if __name__ == '__main__':

    db = Database(r'data')
    db.create_database()
    db.test_database()

    passed_args = get_args()

    try:
        globals()[passed_args.method]()
    except KeyError:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists. Try using the help method ("
              f"e.g. python main.py help)")

    db.close_connection()
