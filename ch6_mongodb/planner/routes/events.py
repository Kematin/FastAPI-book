from fastapi import APIRouter, Body, HTTPException, status
from beanie import PydanticObjectId

from database.connection import Database
from models.events import Event, EventUpdate

from typing import List

event_router = APIRouter(tags=["Events"])
event_database = Database(Event)


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_single_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if event:
        return event
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )


@event_router.post("/new")
async def create_event(new_event: Event = Body(...)) -> dict:
    await event_database.save(new_event)
    return {"message": "Event created successfully."}


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if event:
        return {"message": "Event deleted successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )


@event_router.delete("/")
async def delete_all_events() -> dict:
    events = await event_database.get_all()
    for event in events:
        await event_database.delete(event.id)

    return {"message": "Events delete successfully."}


@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, new_event: EventUpdate) -> Event:
    updated_event = await event_database.update(id, new_event)
    if updated_event:
        return updated_event
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )
