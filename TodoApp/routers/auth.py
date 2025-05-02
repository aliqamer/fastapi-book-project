from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from starlette import status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt


"""
install below packages for hashing passwords
pip install passlib
pip install bcrypt==4.0.1

to submit form data in postman, install below package
pip install python-multipart

to work with JWT tokens, install below package
pip install python-jose[cryptography]

"""

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "2f5fd6270561fa8448d7f125495268d73bd17031a8fd98ac00a275ac58d41077"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# decrpt jwt token
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token") 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str = "user"  # Default role is set to "user"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    
    to_encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    # Here you would typically hash the password and save the user to the database  
    # For now, we'll just return the user data as a response
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),  # In a real app, hash the password
        role=create_user_request.role,
        is_active=True  # Default to active
    )
    
    db.add(create_user_model)
    db.commit()
    # db.refresh(create_user_model)
    

@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(
        username=user.username, user_id=user.id, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {'access_token': token, 'token_type': 'bearer'}
    # return 'Successfully logged in'  # In a real app, return a JWT token or similar