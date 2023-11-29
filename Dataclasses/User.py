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

    def __init__(self, firstname, telephone_number, email, password, role, created_at, children):
        self.firstname = firstname
        self.telephone_number = telephone_number
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
        self.children = children

    def __repr__(self):
        return f"\nRecord: (name:{self.firstname}, phone_num: {self.telephone_number}, email:{self.email}, " \
               f"children: {self.children})"

    def to_array(self):
        return [self.firstname, self.telephone_number, self.email, self.password, self.role, self.created_at,
                self.children]

