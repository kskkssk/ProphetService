from models.request import Request


class RequestService:
    def __init__(self, session):
        self.session = session

    def add_request(self, user_id: int, data:str, model: str):
        new_request = Request(data=data, model=model,user_id=user_id)
        self.session.add(new_request)
        self.session.commit()
        return new_request

    def get_requests_by_user(self, user_id: int):
        return self.session.query(Request).filter(Request.user_id == user_id).all()




