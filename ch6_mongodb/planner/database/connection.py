from beanie import init_beanie, PydanticObjectId, Document
from pydantic import BaseSettings, BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List

from models.users import User
from models.events import Event


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[User, Event])

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model: Document):
        self.model = model

    async def save(self, document) -> None:
        await document.create()

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        else:
            return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc = await self.get(id)
        if not doc:
            return False

        des_body = body.dict()
        des_body = {key: value for key,
                    value in des_body.items() if value is not None}

        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
