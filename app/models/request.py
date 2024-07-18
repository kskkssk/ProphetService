import pandas as pd
from database.database import Base
from sqlalchemy import Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, mapped_column


class Request(Base):
    __tablename__ = 'request'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    data = mapped_column(String)
    model = mapped_column(LargeBinary)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
