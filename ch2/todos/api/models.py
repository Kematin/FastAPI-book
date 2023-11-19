from pydantic import BaseModel


class Item(BaseModel):
    item: str
    status: bool

    class Config:
        json_schema_extra = {
            "example": {
                "item": "example!",
                "status": True
            }
        }


class TodoItem(BaseModel):
    id: int
    item: Item

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "item": {
                    "item": "example!",
                    "status": True
                }
            }
        }
