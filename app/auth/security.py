from datetime import datetime, timedelta

from jose import jwt
from config import (
    pwd_context,
    access_token_expires_delta,
    refresh_token_expires_delta,
    algorithms,
    secret_key
)

from fastapi import HTTPException, status
from jwt import decode, exceptions
from models.users import UserInDB


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict):
    access_to_encode = data.copy()
    refresh_to_encode = data.copy()
    access_token_expires = datetime.utcnow()+timedelta(
        minutes=access_token_expires_delta
    )
    refresh_token_expires = datetime.utcnow()+timedelta(
        days=refresh_token_expires_delta
    )
    access_to_encode.update({"exp": access_token_expires, "type": "access"})
    refresh_to_encode.update({"exp": refresh_token_expires, "type": "refresh"})
    access_token = jwt.encode(
        access_to_encode,
        secret_key,
        algorithm=algorithms
    )
    refresh_token = jwt.encode(
        refresh_to_encode,
        secret_key,
        algorithm=algorithms
    )
    return {"access": access_token, "refresh": refresh_token}


def verify_jwt(token: str) -> UserInDB:
    try:
        decode_token = decode(token, secret_key, algorithms=[algorithms])
        user_id = decode_token.get('id')
        if user_id is not None:
            user = UserInDB(_id=user_id)
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid authentication credentials test')
