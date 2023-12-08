from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event


class User(Document):
    username: str
    password: str
    email: EmailStr
    events: Optional[List[Link[Event]]]

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "username": "kematin",
                "password": "strong!!!",
                "email": "fastapi@google.com",
                "events": []
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@google.com",
                "password": "strong!!!",
            }
        }
