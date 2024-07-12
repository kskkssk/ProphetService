import pandas as pd
from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String)
    model = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    #user = relationship("User", back_populates="request")

    def __init__(self, data, model):
        self.data = data
        self.model = model

    def validate(self):
        try:
            date_obj = pd.to_datetime(self.data, format='%Y-%m-%d')
            return date_obj
        except ValueError:
            raise ValueError('Expected date in the format YYYY-MM-DD')

    def prediction(self):
        date_obj = self.validate()
        future = pd.DataFrame({'ds': pd.date_range(start=date_obj, periods=30)})
        prediction = self.model.predict(future)
        return prediction, self.data
