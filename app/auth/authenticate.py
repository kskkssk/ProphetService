from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/users/signin')


async def authenticate(token) -> str:
    if not token():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Signin for access')
    decoded_token = verify_access_token(token)
    return decoded_token["user"]

