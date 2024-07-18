from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from mlservice.app.services.crud.user_service import UserService
from mlservice.app.services.crud.personal_service import PersonService
from mlservice.app.database.database import get_db
from mlservice.schemas.user import UserCreate, UserResponse, UserSignin
from typing import List

user_route = APIRouter(tags=['User'])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_person_service(user_service: UserService = Depends(get_user_service)) -> PersonService:
    current_user = user_service.get_current_user()
    return PersonService(user_service.session, current_user)

@user_route.post("/signin", response_model=UserResponse)
async def signin(data: UserCreate, user_service: UserService = Depends(get_user_service)):
    if user_service.get_user_by_email(data.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User exists')
    user = user_service.create_user(username=data.username, password=data.password, first_name=data.first_name, last_name=data.last_name, email=data.email)
    return UserResponse.from_orm(user)

@user_route.post("/signup", response_model=UserResponse)
async def signup(data: UserSignin, user_service: UserService = Depends(get_user_service)):
    if not user_service.login(username=data.username, password=data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist')
    return UserResponse.from_orm(user_service.get_current_user())

@user_route.get("/delete_user/{user_id}", response_model=dict)
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        user_service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"message": "User deleted successfully"}

@user_route.get("/get_all_users", response_model=List[UserResponse])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_all_users()
    return [UserResponse.from_orm(user) for user in users]

@user_route.get("/get_user_by_email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_orm(user)

@user_route.get("/get_user_by_id/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_orm(user)

@user_route.get("/transaction_history", response_model=List[dict])
async def transaction_history(person_service: PersonService = Depends(get_person_service)):
    return person_service.transaction_history()

@user_route.get("/current_user", response_model=UserResponse)
async def get_current_user(user_service: UserService = Depends(get_user_service)):
    user = user_service.get_current_user()
    return UserResponse.from_orm(user)

@user_route.post("/handle_request", response_model=dict)
async def handle_request(data: str, model, person_service: PersonService = Depends(get_person_service)):
    try:
        transaction_data = person_service.handle_request(data, model)
        return transaction_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



