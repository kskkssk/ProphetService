from worker.celery_config import app
from services.crud.personal_service import PersonService
from database.database import get_db
from models.user import User


@app.task
def handle_request(data: str, model: str, username: str):
    db = get_db()
    session = next(db)
    try:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            raise ValueError("User not found")
        person_service = PersonService(session, user)
        result = person_service.handle_request(data, model)
        return result
    finally:
        db.close()

