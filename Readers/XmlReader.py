import xml.etree.ElementTree as ElementTree

from Dataclasses.Child import Child
from Dataclasses.User import User
from Readers.Reader import Reader


class XmlReader(Reader):
    file_path = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        data = []

        tree = ElementTree.parse(self.file_path)
        root = tree.getroot()

        for x in root.findall('user'):
            xml_array = []
            child = ''
            for elem in x.iter():
                if elem.tag == 'user' or elem.tag == 'children' or elem.tag == 'child':
                    continue
                if elem.tag == 'name':
                    child += elem.text
                    continue
                if elem.tag == 'age':
                    child += f" {elem.text}"
                    xml_array.append(child)
                    child = ''
                    continue

                xml_array.append(elem.text)

            if self.is_record_initially_invalid(xml_array):
                continue

            phone_num = self.validate_phone_numbers(xml_array[1])
            children = self.__get_children(xml_array[6:])

            data.append(User(xml_array[0], phone_num, xml_array[2], xml_array[3], xml_array[4], xml_array[5], children))

        return data

    @staticmethod
    def __get_children(children_array):
        children = []

        if len(children_array) == 0:
            return children

        for child in children_array:
            name, age = child.split(" ")
            children.append(Child(name, age))

        return children
