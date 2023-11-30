from dataclasses import dataclass
import Dataclasses.Child as Child
from typing import List


@dataclass
class User:
    firstname: str
    telephone_number: str
    email: str
    password: str
    role: str
    created_at: str
    children: List[Child]
    id: int

    def __init__(self, firstname, telephone_number, email, password, role, created_at, children, id=None):
        self.firstname = firstname
        self.telephone_number = telephone_number
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
        self.children = children
        self.id = id

    def __repr__(self):
        return f"Record: (name: {self.firstname}, phone_num: {self.telephone_number}, email: {self.email}, " \
               f"role: {self.role}, created_at: {self.created_at}, children: {self.children})\n"

    def to_array(self):
        return [self.firstname, self.telephone_number, self.email, self.password, self.role, self.created_at,
                self.children]

    @staticmethod
    def from_array(array, children):
        return User(array[0], array[1], array[2], array[3], array[4], array[5], children, array[6])

