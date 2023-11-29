from User import User
from Child import Child
import xml.etree.ElementTree as et


class XmlReader:
    file_path = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        print("------------XML READER")
        data = []

        tree = et.parse(self.file_path)
        root = tree.getroot()
        xml_array = []

        for x in root.findall('user'):
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
            data.append(User(xml_array[0], xml_array[1], xml_array[2], xml_array[3], xml_array[4], xml_array[5], children))
            xml_array = []

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
