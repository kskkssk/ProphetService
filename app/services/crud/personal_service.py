from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import List, Dict
from mlservice.app.models.balance import Balance
from mlservice.app.models.user import User
from mlservice.app.services.crud.balance_service import BalanceService
from mlservice.app.services.crud.request_service import RequestService


class PersonService:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user
        self.balance_service = BalanceService(session)
        self.request_service = RequestService(session)

    def handle_request(self, data: str, model) -> List:
        if self.current_user is None:
            raise ValueError("No user is currently logged in")
        prediction, _ = self.request_service.prediction(data, model)
        spent_sum = 0
        balance = self.balance_service.get_balance(self.current_user.id)
        if balance.amount >= 10:
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

    def add_balance(self, amount: float) -> Balance:
        return self.balance_service.add_balance(self.current_user.id, amount)

    def get_balance(self) -> Balance:
        return self.balance_service.get_balance(self.current_user.id)

    def deduct_balance(self, amount: float) -> Balance:
        return self.balance_service.deduct_balance(self.current_user.id, amount)

    def get_requests_by_user(self) -> List[Dict]:
        return self.request_service.get_requests_by_user(self.current_user.id)