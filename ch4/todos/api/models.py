from pydantic import BaseModel
from typing import List


# Model for the record to db
class Todo(BaseModel):
    id: int
    item: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "item": "example schema!"
            }
        }


# Response model
class TodoItem(BaseModel):
    item: str

    class Config:
        json_schema_extra = {
            "example": {"item": "example schema!"}
        }


# Response model
class TodoItems(BaseModel):
    tasks: List[TodoItem]

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {"item": "schema 1"},
                    {"item": "schema 2"},
                    {"item": "schema 3"},
                ]
            }
        }
