import argparse
import sys


def print_hi():
    print(f'Hi, tomek')


def help():
    # prints all commands
    print("todo")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--login')
    parser.add_argument('--password')
    parser.add_argument('method')

    args, unknown = parser.parse_known_args()
    # print(f'UNKNOWN {unknown}')

    return args


if __name__ == '__main__':
    passed_args = get_args()
    # print(f"passed args:{passed_args}")
    # print({'login': passed_args.login, 'password': passed_args.password})

    try:
        globals()[passed_args.method]()
    except KeyError:
        print(f"\n ERROR: No function called {passed_args.method} exists. Try using the help method (e.g. python "
              f"main.py help)")
