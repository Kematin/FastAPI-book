from pydantic import BaseModel


class Item(BaseModel):
    item: str
    status: bool


class TodoItem(BaseModel):
    id: int
    item: Item
