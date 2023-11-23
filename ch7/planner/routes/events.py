# FastAPI, MongoDB
from fastapi import APIRouter, Body, HTTPException, status, Depends
from beanie import PydanticObjectId

# DB, Models
from database.connection import Database
from models.events import Event, EventUpdate

# AUTH
from auth.authenticate import authenticate

# Other
from typing import List

event_router = APIRouter(tags=["Events"])
event_database = Database(Event)


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_single_event(id: PydanticObjectId,
                                user: str = Depends(authenticate)) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You dont have permission to get this event."
        )
    else:
        return event


@event_router.post("/new")
async def create_event(new_event: Event, user: str = Depends(authenticate)) -> dict:
    new_event.creator = user
    await event_database.save(new_event)
    return {"message": "Event created successfully."}


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You dont have permission to delete this event."
        )
    else:
        await event_database.delete(id)
        return {"message": "Event deleted successfully."}


@event_router.delete("/")
async def delete_all_events(user: str = Depends(authenticate)) -> dict:
    events = await event_database.get_all()
    for event in events:
        if event.creator != user:
            continue
        await event_database.delete(event.id)

    return {"message": "Events delete successfully."}


@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, new_event: EventUpdate,
                       user: str = Depends(authenticate)) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You dont have permission to change this event."
        )
    else:
        updated_event = await event_database.update(id, new_event)
        return updated_event
