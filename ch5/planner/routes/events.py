from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List

event_router = APIRouter(tags=["Events"])

events = []


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_single_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )


@event_router.post("/new")
async def create_event(data: Event = Body(...)) -> dict:
    try:
        data.id = events[-1].id + 1
    except IndexError:
        data.id = 1

    events.append(data)
    return {"message": "Event created successfully."}


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {"message": "Event deleted successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "Events delete successfully."}
