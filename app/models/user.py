from typing import Dict
from sqlalchemy import Column, Integer, String, JSON, Float
from .request import Request
from database.database import Base  # Adjust the number of dots based on the relative path
from sqlalchemy.orm import relationship
from models.balance import Balance


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False, default=0.0)
    balance = relationship("Balance", uselist=False, back_populates="user")
    transaction_list = Column(JSON)

    def __init__(self, username: str, password: str, first_name: str, last_name: str, email: str, amount: float = 0.0):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.transaction_list = []
        self.amount = amount

    def add_transaction(self, transaction: Dict):
        self.transaction_list.append(transaction)

    def transaction_history(self):
        return self.transaction_list