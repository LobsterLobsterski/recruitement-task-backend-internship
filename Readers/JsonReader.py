import json

from Dataclasses.Child import Child
from Dataclasses.User import User
from Readers.Reader import Reader


class JsonReader(Reader):
    file_path = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        data = []
        with open(self.file_path) as f:
            lines = json.load(f)
            for line in lines:
                line = list(line.values())

                if self.is_record_initially_invalid(line):
                    continue

                children = self.__get_children(line[6])
                phone_num = self.validate_phone_numbers(line[1])

                record = User(line[0], phone_num, line[2], line[3], line[4], line[5], children)
                data.append(record)

        return data

    @staticmethod
    def __get_children(children_array):
        children = []

        if len(children_array) == 0:
            return children

        for child_dict in children_array:
            children.append(Child(child_dict['name'], child_dict['age']))

        return children
