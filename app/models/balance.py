class Balance:
    def __init__(self, balance):
        self.__balance = balance

    def check_balance(self) -> float:
        return self.__balance

    def add_balance(self, amount: float):
        self.__balance += amount
        return self.__balance

    def deduct_balance(self, amount: float) -> bool:
        if amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
