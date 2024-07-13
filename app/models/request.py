import pandas as pd
from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column


class Request(Base):
    __tablename__ = 'request'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    data = mapped_column(String)
    model = mapped_column(String)
    user_id = mapped_column(Integer, ForeignKey('users.id'))

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
        future = pd.DataFrame({'ds': pd.date_range(start=date_obj, periods=5)})
        prediction = self.model.predict(future)
        prediction['ds'] = prediction['ds'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return prediction, self.data
