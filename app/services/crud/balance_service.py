from models.balance import Balance


class BalanceService:
    def __init__(self, session):
        self.session = session

    def add_balance(self, user_id: int, amount: float) -> float:
        balance = self.session.query(Balance).filter_by(user_id=user_id).first()
        if balance:
            balance.amount += amount
            self.session.commit()
            return balance.amount
        else:
            raise ValueError(f"Баланс для пользователя {user_id} не найден")

    def get_balance(self, user_id: int) -> float:
        balance = self.session.query(Balance).filter_by(user_id=user_id).first()
        if balance:
            return balance.amount
        else:
            raise ValueError(f"Баланс для пользователя {user_id} не найден")
