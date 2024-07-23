from worker.celery_config import app
from services.crud.user_service import UserService
from services.crud.personal_service import PersonService
from database.database import get_db
from models.user import User


@app.task
def handle_request(data: str, model: str, user_id: int):
    db = get_db()
    session = next(db)
    try:
        user = session.query(User).get(user_id)
        if user is None:
            raise ValueError("User not found")
        person_service = PersonService(session, user)
        return person_service.handle_request(data, model)
    finally:
        db.close()

