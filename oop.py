class Person:
    name = "Person"  # поля класу
    attack = 0  # поля класу
    speed = 15  # поля класу

    def __init__(self, name1, attack1, speed1):


        self.name = name1
        self.attack = attack1
        self.speed = speed1

    def __str__(self):
        return (f"I am {self.name} and my {self.attack=} "
                f"and my {self.speed=}")


    def say_name(self):  # метод класу
        print(self.name)


criper = Person("Cryper", 500, 50)
criper.say_name()
# zombie = Person()
# zombie.say_name()
# zombie.name = "Zombie"
# zombie.say_name()
print(criper)
