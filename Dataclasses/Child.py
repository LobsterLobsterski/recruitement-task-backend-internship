from dataclasses import dataclass


@dataclass
class Child:
    name: str
    age: int
    id: int

    def __init__(self, name, age, id=None):
        self.name = name
        self.age = age
        self.id = id

    @staticmethod
    def from_array(array):
        return Child(array[0], array[1], array[2])

    def __repr__(self):
        return f"Child(name:{self.name}, age:{self.age})"

    def __hash__(self):
        return hash(f"{self.name}{self.age}{self.id}")
