class Car:
    name = ""
    sped = 50
    pollution = ""

    def __init__(self, name, pollution = "average", sped = 50):
        self.name = name
        self.sped = sped
        self.pollution = pollution

class Electric_Сar(Car):
    def show_car_info(self):
        print(f"electric car {self.name}, with a maximum speed of {self.sped} km/h")
    def pollution_power(self):
        print(f"pollution power electric car {self.name}: {self.pollution}")

class Hybrid_Сar(Car):
    def show_car_info(self):
        print(f"car hybrid {self.name}, with a maximum speed of {self.sped} km/h")
    def pollution_power(self):
        print(f"pollution power hybrid {self.name}: {self.pollution}")

class Gasoline_Сar(Car):
    def show_car_info(self):
        print(f"gasoline car {self.name}, with a maximum speed of {self.sped} km/h")
    def pollution_power(self):
        print(f"pollution power Gasoline {self.name}: {self.pollution}")

Tesla_Model_3 = Electric_Сar("Tesla Model 3", sped=225, pollution="above average")
Tesla_Model_3.show_car_info()
Tesla_Model_3.pollution_power()
print("\n")
Toyota_Corolla = Hybrid_Сar("Toyota Corolla", sped=200, pollution="average")
Toyota_Corolla.show_car_info()
Toyota_Corolla.pollution_power()
print("\n")
Toyota_RAV4 = Gasoline_Сar("Toyota RAV4", sped=200, pollution="high")
Toyota_RAV4.show_car_info()
Toyota_RAV4.pollution_power()