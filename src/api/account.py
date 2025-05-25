from fastapi import APIRouter, Depends, HTTPException, status
import bcrypt
import sqlalchemy
from src.api import auth
from src import database as db
from pydantic import BaseModel

router = APIRouter(
    prefix="/account",
    tags=["account"],
    dependencies=[Depends(auth.get_api_key)],
)


class User(BaseModel):
    username: str
    password: str


class Creationresponse(BaseModel):
    id: int


@router.post(
    "/new", response_model=Creationresponse, status_code=status.HTTP_201_CREATED
)
def create_new(user: User):
    """
    Create a new account by setting a username and password. Returns the id of the newly created account.
    """
    hashed_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO account_users (username, password) 
                VALUES (:username, :password) 
                RETURNING id
                """
            ),
            {"username": user.username, "password": hashed_pw},
        ).one()
        
    return Creationresponse(id=result[0])


@router.post(
    "/login", response_model=Creationresponse, status_code=status.HTTP_201_CREATED
)
def login_user(user: User):
    """
    Login to an existing account using username and password to fetch the id of the account.
    """

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, password FROM account_users 
                WHERE username = :username
                """
            ),
            {"username": user.username},
        ).one_or_none()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password. User not found in the database.",
            )
        
        #check password
        if not bcrypt.checkpw(user.password.encode("utf-8"), result[1].encode("utf-8")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )
         
         

    return Creationresponse(id=result[0])
