from mlservice.models.user import User
from mlservice.models.request import Request
from typing import List
import hashlib


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
