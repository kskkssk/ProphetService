from typing import Dict
from sqlalchemy import Column, Integer, String, JSON
from database.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    balance = relationship("Balance", back_populates="user")
    requests = relationship("Request", back_populates="user")
    transaction_list = Column(JSON)

    def __init__(self, username: str, first_name: str, last_name: str, balance: float, email: str):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.balance = balance
        self.transaction_list = []

    def add_transaction(self, transaction: Dict):
        self.__transaction_list.append(transaction)

    def transaction_history(self):
        return self.__transaction_list