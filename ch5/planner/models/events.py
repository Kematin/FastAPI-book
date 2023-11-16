from pydantic import BaseModel
from typing import List


class Event(BaseModel):
    id: int
    title: str
    description: str
    location: str
    image_url: str
    tags: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastApi book",
                "description": "Book include FastApi content",
                "location": "Google Meet",
                "image_url": "https://m.media-amazon.com/images/I/31lhdB3tb0L.jpg",
                "tags": ["python", "fastapi", "web"]
            }
        }
