from prophet import Prophet
import joblib
import pandas as pd


class RequestService:
    def __init__(self, session):
        self.session = session

    def validate(self, data: str):
        try:
            date_obj = pd.to_datetime(data, format='%Y-%m-%d')
            return date_obj
        except ValueError:
            raise ValueError('Expected date in the format YYYY-MM-DD')

    def load_prophet_model(self, model_path: str) -> Prophet:
        model_path = 'prophet_model.pkl'
        with open(model_path, 'rb') as f:
            model = joblib.load(f)
        return model

    def prediction(self, data: str, model_path: str):
        prophet_model = self.load_prophet_model(model_path)
        date_obj = self.validate(data)
        future = pd.DataFrame({'ds': pd.date_range(start=date_obj, periods=5)})
        prediction = prophet_model.predict(future)
        prediction['ds'] = prediction['ds'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return prediction, data


