from Dataclasses.Child import Child
from Readers.Reader import Reader
from Dataclasses.User import User


class CsvReader(Reader):
    file_path = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path) as f:
            data = []
            lines = f.read().split("\n")[1:]
            for line in lines:
                split_line = line.split(";")

                if split_line[1] == '' or not self.is_email_valid(split_line[2]):
                    continue

                phone_num = self.validate_phone_numbers(split_line[1])

                if len(split_line) == 6:
                    record = User(split_line[0], phone_num, split_line[2], split_line[3], split_line[4], split_line[5])
                else:
                    children = self.__get_children(split_line[6])
                    record = User(split_line[0], phone_num, split_line[2], split_line[3], split_line[4], split_line[5],
                                  children)

                data.append(record)

            return data

    @staticmethod
    def __get_children(children_string):
        children = []

        if children_string == '':
            return children

        for child in children_string.split(","):
            name, age = child.split(" ")
            age = age.replace(")", "").replace("(", "")
            children.append(Child(name, age))

        return children
