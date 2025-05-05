from fastapi import APIRouter, Depends, status
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

    with db.engine.begin() as connection:
        id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO account_users (username, password) 
                VALUES (:username, :password) 
                RETURNING id
                """
            ),
            {"username": user.username, "password": user.password},
        ).one()

    return Creationresponse(id=id[0])


@router.post(
    "/login", response_model=Creationresponse, status_code=status.HTTP_201_CREATED
)
def login_user(user: User):
    """
    Login to an existing account using username and password to fetch the id of the account.
    """

    with db.engine.begin() as connection:
        id = connection.execute(
            sqlalchemy.text(
                """
                SELECT id FROM account_users 
                WHERE username = :username AND password = :password
                """
            ),
            {"username": user.username, "password": user.password},
        ).one()

    return Creationresponse(id=id[0])
