from typing import List, Dict
import pandas as pd
from datetime import datetime
from prophet import Prophet
import joblib
import hashlib


class Request:
    def __init__(self, data, model):
        self.data = data
        self.__model = model

    def validate(self):
        try:
            date = pd.to_datetime(self.data, format='%Y-%m-%d')
            return date
        except ValueError:
            raise ValueError('Ожидается дата в формате YYYY-MM-DD')

    def prediction(self):
        date = self.validate()
        future = pd.DataFrame({'ds': pd.date_range(start=date, periods=30)})
        prediction = self.__model.predict(future)
        return prediction, self.data


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


class UserService:
    users_db = {}

    def __init__(self):
        self.current_user = None

    def _hash_password(self, password):
        password = password.encode('utf-8')
        hash_object = hashlib.sha256(password)
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def sign_in(self, username, password):
        if username not in self.users_db:
            print("User doesn't exist")
            return False
        hashed_password = self._hash_password(password)
        if self.users_db[username]['password'] == hashed_password:
            self.current_user = self.users_db[username]['user']
            print("Successfully signed in")
            return True
        else:
            print("Wrong password. Try again")
            return False

    def sign_up(self, username: str, password: str, first_name: str, last_name: str, balance: float, email: str):
        if username in self.users_db:
            print("User already exists")
            return False
        new_user = User(username, first_name, last_name, balance, email)
        self.users_db[username] = {}
        self.users_db[username]['user'] = new_user
        self.users_db[username]['password'] = self._hash_password(password)
        print("Successfully signed up")
        return True

    def handle_request(self, request: Request) -> List:
        if self.current_user is None:
            return False
        prediction, data = request.prediction()
        spent_sum = 0
        if self.current_user.deduct_balance(10):
            spent_sum += 10
            transaction = {
                'spent_money': spent_sum,
                'prediction': prediction.to_dict(orient='records'),
                'data': data
            }
            self.current_user.add_transaction(transaction)
        return transaction

    def transaction_history(self):
        return self.current_user.transaction_history()


if __name__ == '__main__':
    model = joblib.load('/home/sasha/PycharmProjects/MLserver/pythonProject2/mlservice/prophet_model.pkl')
    #Пример
    service = UserService()
    service.sign_up('kskkssk', '0880', 'Aleks', 'Kud', 20, 'example@gmail.com')
    service.sign_in('kskkssk', '0880')
    request = Request('2024-02-27', model)
    transaction = service.handle_request(request)
    if transaction:
        print(transaction)
    else:
        print("Ошибка")

    print('История транзакций', service.transaction_history())