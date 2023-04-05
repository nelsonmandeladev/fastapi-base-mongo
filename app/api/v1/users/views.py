from config import project_db, algorithms, pwd_context, secret_key
from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from auth.security import get_password_hash, create_token
from models.users import UserCreate, UserResponse
from models.token import TokenResponse
import jwt
router = APIRouter()


user_collection = project_db["users"]


@router.post("", response_model=UserResponse)
async def create_user(email: EmailStr, password: str):
    hashed_password = get_password_hash(password=password)
    user = UserCreate(email=email, password=hashed_password)
    user_collection.insert_one(user.dict())
    return user


@router.post("/login", response_model=TokenResponse)
async def login(email: str, password: str):
    user = project_db.users.find_one(
        {"$or": [{"email": email}, {"email": email}]}
    )

    if user:
        if pwd_context.verify(password, user.get('password')):
            payload = {"id": str(user.get('_id'))}
            token = create_token(data=payload)
            # Return token to client
            return token
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or email")
