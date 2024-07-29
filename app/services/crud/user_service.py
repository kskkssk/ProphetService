from models.user import User
from models.balance import Balance
from services.crud.request_service import RequestService
from services.crud.balance_service import BalanceService
from typing import List, Optional
from sqlalchemy.orm.attributes import flag_modified
from passlib.context import CryptContext
from auth.jwt_handler import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

current_user = None


class UserService:
    def __init__(self, session):
        global current_user
        self.session = session
        self.current_user: Optional[User] = current_user
        self.balance_service = BalanceService(session)
        self.request_service = RequestService(session)

    def _hash_password(self, password: str):
        hashed_password = pwd_context.hash(password)
        return hashed_password

    def create_user(self, username: str, password: str, first_name: str, last_name: str, email: str, balance: float = 0.0) -> User:
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            raise ValueError("User already exists")
        email_exists = self.session.query(User).filter_by(email=email).first()
        if email_exists:
            raise ValueError(f"User with email {email} already exists")
        new_user = User(username=username,
                        password=self._hash_password(password),
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        transaction_list=[])
        self.session.add(new_user)
        self.session.commit()
        user_balance = Balance(amount=balance, user_id=new_user.id)
        self.session.add(user_balance)
        self.session.commit()
        return new_user

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
        else:
            raise ValueError(f"User with id {user_id} not found")

    def login(self, email: str, password: str) -> dict:
        global current_user
        user = self.session.query(User).filter_by(email=email).first()
        if user is None:
            raise ValueError("User doesn't exist")
        if pwd_context.verify(password, user.password):
            current_user = user
            self.current_user = user
            access_token = create_access_token(user.email)
            return {"access_token": access_token, "token_type": "Bearer"}
        else:
            raise ValueError("Wrong password. Try again")

    def handle_request(self, data: str, model) -> List:
        if self.current_user is None:
            raise ValueError("No user is currently logged in")

        prediction, _ = self.request_service.prediction(data, model)
        spent_sum = 0

        if self.balance_service.deduct_balance(user_id=self.current_user.id, amount=10):
            spent_sum += 10
            transaction_data = {
                'spent_money': spent_sum,
                'prediction': prediction.to_dict(orient='records'),
                'data': data
            }

            self.current_user.transaction_list.append(transaction_data)
            flag_modified(self.current_user, "transaction_list")
            self.session.commit()
            return transaction_data
        else:
            raise ValueError("Not enough balance")

    def transaction_history(self) -> List[dict]:
        if self.current_user is None:
            raise ValueError("No user is currently logged in")
        return self.current_user.transaction_list

    def get_current_user(self) -> User:
        if self.current_user is None:
            raise ValueError("No user is currently logged in")
        return self.current_user

    def logout(self):
        global current_user
        current_user = None
        self.current_user = None
