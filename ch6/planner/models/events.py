from sqlmodel import JSON, SQLModel, Field, Column
from typing import List, Optional
from pydantic import BaseModel


class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    location: str
    image_url: str
    tags: List[str] = Field(sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "title": "FastApi book",
                "description": "Book include FastApi content",
                "location": "Google Meet",
                "image_url": "https://m.media-amazon.com/images/I/31lhdB3tb0L.jpg",
                "tags": ["python", "fastapi", "web"]
            }
        }


class EventUpdate(SQLModel):
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]
    image_url: Optional[str]
    tags: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "title": "FastApi book v.2",
                "description": "Book include new version FastApi content",
                "location": "Google Meet",
                "image_url": "https://m.media-amazon.com/images/I/31lhdB3tb0L.jpg",
                "tags": ["python", "fastapi", "web", "http", "rest"]
            }
        }
