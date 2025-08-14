class Person:
    name = "Person"  # поля класу
    old = 0  # поля класу
    weight = 15  # поля класу
    bark = ""

    def __init__(self, name1, old1, weight1, bark1):


        self.name = name1
        self.old = old1
        self.weight = weight1
        self.bark = bark1

    def __str__(self):
        return (f"I am {self.name} and my yers {self.old=}, "
                f"my {self.weight=}. {self.bark=}")


    def say_name(self):  # метод класу
        print(self.name)

Dog = Person("Hot-Dog", 200, 3000, "Woof-Woof")
Dog.say_name()
print(Dog)