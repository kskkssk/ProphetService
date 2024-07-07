from mlservice.balance import Balance
from typing import Dict


class User:
    def __init__(self, username: str, first_name: str, last_name: str, balance: float, email: str):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.__balance = Balance(balance)
        self.__transaction_list = []

    def get_balance(self):
        return self.__balance.check_balance()

    def add_balance(self, amount: float):
        return self.__balance.add_balance(amount)

    def deduct_balance(self, amount: float):
        return self.__balance.deduct_balance(amount)

    def add_transaction(self, transaction: Dict):
        self.__transaction_list.append(transaction)

    def transaction_history(self):
        return self.__transaction_list
