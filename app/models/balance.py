from database.database import Base
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Balance(Base):
    __tablename__ = 'balance'

    amount = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="balance")

    def deduct_balance(self, amount: float) -> bool:
        if amount <= self.amount:
            self.amount -= amount
            return True
        return False

