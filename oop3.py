class Car:
    name = ""
    speed = 50
    pollution = ""

    def __init__(self, name, pollution = "average", speed = 50):
        self.name = name
        self.speed = speed
        self.pollution = pollution

class ElectricСar(Car):
    def show_car_info(self):
        print(f"electric car {self.name}, with a maximum speed of {self.speed} km/h")
    def pollution_power(self):
        print(f"pollution power electric car {self.name}: {self.pollution}")

class HybridСar(Car):
    def show_car_info(self):
        print(f"car hybrid {self.name}, with a maximum speed of {self.speed} km/h")
    def pollution_power(self):
        print(f"pollution power hybrid {self.name}: {self.pollution}")

class GasolineСar(Car):
    def show_car_info(self):
        print(f"gasoline car {self.name}, with a maximum speed of {self.speed} km/h")
    def pollution_power(self):
        print(f"pollution power Gasoline {self.name}: {self.pollution}")

tesla_model_3 = ElectricСar("Tesla Model 3", speed=225, pollution="above average")
tesla_model_3.show_car_info()
tesla_model_3.pollution_power()
print("\n")
toyota_corolla = HybridСar("Toyota Corolla", speed=200, pollution="average")
toyota_corolla.show_car_info()
toyota_corolla.pollution_power()
print("\n")
toyota_RAV4 = GasolineСar("Toyota RAV4", speed=200, pollution="high")
toyota_RAV4.show_car_info()
toyota_RAV4.pollution_power()