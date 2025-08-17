class BankAccount:
    def __init__(self, passport, balance, name):
        self.__passport = passport
        self.__balance = balance
        self.__name = name

    def info(self):
        print(self.__balance, self.__name)

    def get_passport(self):
        return self.__passport

    def set_balance(self, new_balance):
        if new_balance <= 0:
            return "Error"
        else:
            self.__balance = new_balance
            return self.__balance