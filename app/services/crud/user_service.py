from models.user import User
from models.request import Request
from typing import List, Optional
import hashlib
from database.database import Base, SessionLocal


class UserService(Base):
    def __init__(self, session):
        self.current_user: Optional[User] = None
        self.session = session

    def _hash_password(self, password):
        password = password.encode('utf-8')
        hash_object = hashlib.sha256(password)
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def create_user(self, username: str, password: str, first_name: str, last_name: str, email: str, balance=0):
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            print("User already exists")
            return False
        new_user = User(username=username,
                        password=self._hash_password(password),
                        first_name=first_name,
                        last_name=last_name,
                        balance=balance,
                        email=email,
                        transaction_list=[])
        self.session.add(new_user)
        self.session.commit()
        print("Successfully signed up")
        return True

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
        else:
            raise ValueError(f"User with id {user_id} not found")

    def login(self, username: str, password: str):
        user = self.session.query(User).filter_by(username=username).first()
        if user is None:
            print("User doesn't exist")
            return False
        hashed_password = self._hash_password(password)
        if user.password == hashed_password:
            self.current_user = user
            print("Successfully signed in")
            return True
        else:
            print("Wrong password. Try again")
            return False

    def handle_request(self, request: Request) -> List:
        if self.current_user is None:
            return False
        prediction, data = request.prediction()
        spent_sum = 0
        if self.current_user.balance.deduct_balance(10):
            spent_sum += 10
            transaction = {
                'spent_money': spent_sum,
                'prediction': prediction.to_dict(orient='records'),
                'data': data
            }
            self.current_user.add_transaction(transaction)
            self.session.commit()
            return transaction
        else:
            return None

    def transaction_history(self):
        if self.current_user:
            return self.current_user.transaction_history()
        else:
            return None
