from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router = APIRouter(tags=["User"])

users = {}


@user_router.post("/signup")
async def sign_new_user(data: User) -> dict:
    if data.email in users or data.username in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with current data already exist."
        )

    users[data.email] = data
    return {"message": "User successfully registered!"}


@user_router.post("/signin")
async def sign_user(user: UserSignIn) -> dict:
    if users.get(user.email) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed."
        )

    return {"message": "User signed in successfully."}


@user_router.get("/list")
async def get_list_users() -> dict:
    return users
