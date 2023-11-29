import xml.etree.ElementTree as ElementTree

from Dataclasses.Child import Child
from Readers.Reader import Reader
from Dataclasses.User import User


class XmlReader(Reader):
    file_path = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        print("------------XML READER")
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

            children = self.__get_children(xml_array[6:])

            if xml_array[1] == '' or not self.is_email_valid(xml_array[2]):
                # print(f"\t bad record: phone={xml_array[1]}, mail={xml_array[2]}")
                continue

            # print("\tgood record")
            phone_num = self.validate_phone_numbers(xml_array[1])

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
