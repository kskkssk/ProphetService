from typing import List, Dict
import joblib
import pandas as pd
from datetime import datetime
from prophet import Prophet


class Request:
    def __init__(self, data, model):
        self.data = data
        self.model = model

    def validate(self):
        try:
            date = pd.to_datetime(self.data, format='%Y-%m-%d')
            return date
        except ValueError:
            raise ValueError('Ожидается дата в формате YYYY-MM-DD')

    def prediction(self):
        date = self.validate()
        future = pd.DataFrame({'ds': [date]})
        prediction = self.model.predict(future)
        return prediction, self.data


class User:
    def __init__(self, username: str, first_name: str, last_name: str, balance: float, password: str):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.__balance = balance
        self.transaction_list = {}

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

    def transaction_history(self) -> List[Dict]:
        return self.transaction_list

    def handle_request(self, request: Request):
        prediction, data = request.prediction()
        count_sum = 0
        if self.deduct_balance(10):
            count_sum += 10
            self.transaction_list['spent_money'] = count_sum
            self.transaction_list['prediction'] = prediction.to_dict(orient='records')
            self.transaction_list['data'] = data
        return self.transaction_list


m = joblib.load('prophet_model.pkl')

if __name__ == '__main__':
    #Пример
    user = User('kk', 'Aleks', 'Kud', 10, '0880')
    request = Request('2024-02-27', m)
    try:
        result = user.handle_request(request)
    except:
        raise ValueError("Ошибка")

    print('История транзакций', user.transaction_history())