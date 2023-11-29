from User import User
from Child import Child
import json


class JsonReader:
    file_path = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        data = []
        with open(self.file_path) as f:
            lines = json.load(f)
            for line in lines:
                line = list(line.values())
                children = self.__get_children(line[6])
                record = User(line[0], line[1], line[2], line[3], line[4], line[5], children)
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
