from sqlalchemy import Integer, String, JSON
from database.database import Base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship, mapped_column


class User(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True, nullable=False)
    first_name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)

    balance = relationship("Balance", uselist=False, back_populates="user")
    transaction_list = mapped_column(JSON, default=list, nullable=False)

