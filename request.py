class Request:
    def __init__(self, data, model):
        self.data = data
        self._model = model

    def validate(self):
        try:
            date = pd.to_datetime(self.data, format='%Y-%m-%d')
            return date
        except ValueError:
            raise ValueError('Ожидается дата в формате YYYY-MM-DD')

    def prediction(self):
        date = self.validate()
        future = pd.DataFrame({'ds': pd.date_range(start=date, periods=30)})
        prediction = self._model.predict(future)
        return prediction, self.data
