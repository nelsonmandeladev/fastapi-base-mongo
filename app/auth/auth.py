from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.users import UserInDB
from .security import verify_jwt


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserInDB:
    try:
        if credentials and credentials.scheme == "Bearer":
            token = credentials.credentials
            user = verify_jwt(token)
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Bearer token most be provided in the request header'
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='auth token expired or not valid, please request a new one!'
        )
