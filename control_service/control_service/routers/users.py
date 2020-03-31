from fastapi import APIRouter, Depends, HTTPException, status
from control_service.models import UserData, sql_userdata,database,TokenData,Token,RegisterUser
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
import aiodns
import re

# to get a string like this run:
# openssl rand -hex 32

SECRET_KEY = os.environ.get("SECRET_KEY","09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7") # just for testing
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Login")
router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(username: str):
    query = sql_userdata.select().where(sql_userdata.c.UserName==username)
    result= await database.fetch_one(query)
    print(result)
    if result:
        return result

async def authenticate_user( username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    jwt.encode(to_encode, SECRET_KEY)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserData = Depends(get_current_user)):
    if current_user.Enabled is False:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


@router.post("/Login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.Enabled is False:
        raise HTTPException(status_code=403, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.UserName}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/Register')
async def register(data: RegisterUser):

    response = {}
    query = sql_userdata.select().where(sql_userdata.c.UserName == data.UserName)
    query2 = sql_userdata.select().where(sql_userdata.c.Email == data.Email)
    result = await database.fetch_one(query)
    result2 = await database.fetch_one(query2)
    if result is not None:
        response['Success'] = False
        response['Reason'] = "Username taken"
        return response
    elif result2 is not None:
        response['Success'] = False
        response['Reason'] = "Email taken"
        return response
    else:
        if not re.match(".+@[\w\.]+\..+",data.Email):
            response['Success'] = False
            response['Reason'] = "no right email format"
            return response
        try:
            resolver = aiodns.DNSResolver()
            email_hostname = data.Email[data.Email.find('@') + 1:]
            MX_DNS = await  resolver.query(email_hostname, 'MX')
        except aiodns.error.DNSError as e:
            MX_DNS = None
        print(MX_DNS)
        if MX_DNS is None:
            response['Success'] = False
            response['Reason'] = "Email server not available"
            return response


        query=sql_userdata.insert().values(
            UserName=data.UserName,
            password=get_password_hash(data.password),
            Email=data.Email,
            Telefon=data.Telefon,
            Enabled=False
        )
        await database.execute(query)
        response['Success'] = True
        return response

@router.get('/GetUserProfil')
async def getUserProfil(current_user: UserData = Depends(get_current_user)):
    if current_user.Enabled is False:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user
