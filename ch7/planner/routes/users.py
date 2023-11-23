# FastAPI, main libs
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from beanie import PydanticObjectId

# AUTH
from auth.hash_password import HashPassowrd
from auth.jwt_handler import create_access_token

# DB, models
from database.connection import Database
from models.users import User, TokenResponse

# Other
from typing import List

user_router = APIRouter(tags=["User"])
users_database = Database(User)
user_hash_password = HashPassowrd()


@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with current data already exist."
        )

    hashed_password = user_hash_password.create_hash(user.password)
    user.password = hashed_password
    await users_database.save(user)
    return {"message": "User successfully registered!"}


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user(user: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user_exist = (await User.find_one(User.email == user.username)) or \
        (await User.find_one(User.username == user.username))
    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    if not user_hash_password.verify_hash(user.password, user_exist.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed."
        )
    access_token = create_access_token(user_exist.email)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }


@user_router.delete("/{id}")
async def delete_user(id: PydanticObjectId) -> dict:
    result = await users_database.delete(id)
    if result:
        return {"message": "User was deleted successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found."
        )


@user_router.get("/list")
async def get_list_users() -> List[User]:
    users = await users_database.get_all()
    return users
