import argparse
import os


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

def get_all_datafiles_paths(dir_path):
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            datafile_paths.append(dir_path+"\\"+path)
        else:
            get_all_datafiles_paths(os.path.join(dir_path, path))


if __name__ == '__main__':

    datafile_paths = []
    get_all_datafiles_paths(r'data')
    print(datafile_paths)

    passed_args = get_args()
    # print(f"passed args:{passed_args}")
    # print({'login': passed_args.login, 'password': passed_args.password})

    try:
        globals()[passed_args.method]()
    except KeyError:
        print(f"\n ERROR: Function \033[1m{passed_args.method}\033[0m doesn't exists. Try using the help method ("
              f"e.g. python main.py help)")
