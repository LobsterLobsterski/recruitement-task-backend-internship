from dataclasses import dataclass


@dataclass
class Child:
    name: str
    age: int

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Child(name:{self.name}, age:{self.age})"
