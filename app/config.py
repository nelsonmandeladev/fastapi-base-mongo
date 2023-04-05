import secrets
import pymongo
from passlib.context import CryptContext

secret_key = "4acd45f756069e27f0eae840c21d36ed272fce650117d997f7052c85467d074f7dd984e34ccac7aeb12119557cb938717b5f0b4466e3c76996936b4f5b9b70fc"
algorithms = "HS256"
client = pymongo.MongoClient("mongodb://localhost:27017/")
project_db = client["mydatabase"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# value in minutes
access_token_expires_delta: int = 15
# Value in day
refresh_token_expires_delta: int = 30
