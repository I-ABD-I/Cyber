class Animal:
    name: str
    age: int

    def __init__(self, name: str, age: int = 0):
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1

    def get_age(self) -> int:
        return self.age

    def __str__(self) -> str:
        return f"Animal {self.name} is {self.age} years old."


if __name__ == "__main__":
    for i in range(1, 5):
        a = Animal("n" * i, i)
        print(a)
