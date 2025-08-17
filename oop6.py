from datetime import datetime, timedelta

class Human:
    def __init__(self, title, hp, stamina, speed, level, attack, reload_time, role = ''):
        self.title = title
        self.hp = hp
        self.stamina = stamina
        self.speed = speed
        self.level = level
        self.attack = attack
        self.reload_time = reload_time
        self.last_attack = None
        self.role = role

    def __str__(self) -> str:
        return f"Race: {self.title}"

    def check_attack(self):
        if self.last_attack and ((datetime.now() - self.last_attack) < timedelta(microseconds=self.reload_time)):
            return False
        else:
            return True

    def attack_func(self):
        if self.check_attack():
            self.last_attack = datetime.now()
            print(f"{self.role} attacking {self.attack}")
            return self.attack
        else:
            print(f"{self.role}: pls, wait!")
            return 0

class Archer(Human):
    def __init__(self, level, role = ''):
        self.title = "Archer"
        super().__init__(self.title, 80 + level*20, 95 + level*5, 3, level, 40 + level*5, 3, role)


class Knight(Human):
    def __init__(self, level, role = ''):
        self.title = "Knight"
        super().__init__(self.title, 80 + level*20, 105 + level*5, 5, level, 45 + level*5, 3, role)


class Wizard(Human):
    def __init__(self, level, role = ''):
        self.title = "Wizard"
        super().__init__(self.title, 80 + level*20, 95 + level*5, 3, level, 40 + level*5, 3, role)


print("Welcome to game!")
name = input("Enter your name> ")
answer = 0
while answer not in [1, 2, 3]:
    answer = int(input("Choose role\n 1: Archer, 2: Knight, 3: Wizard> "))
    if answer == 1:
        hero = Archer(level=1, role='Hero')
    elif answer == 2:
        hero = Knight(level=1, role='Hero')
    elif answer == 3:
        hero = Wizard(level=1, role='Hero')
    else:
        print("Error! Try again")

print(hero)

enemy1 = Knight(1, 'Enemy')
print(f"Your enemy is {enemy1} HP is {enemy1.hp}")

while enemy1.hp > 0 and hero.hp > 0:
    print(f"Enemy hp {enemy1.hp}, hero hp {hero.hp}")
    enemy1.hp -= hero.attack_func()
    if enemy1.hp > 0:
        hero.hp -= enemy1.attack_func()


if enemy1.hp <= 0:
    print("You win!")
else:
    print("You lost!")
