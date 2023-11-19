from fastapi import APIRouter, Depends, Body, HTTPException, status, Request
from sqlalchemy import select
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List, Dict

event_router = APIRouter(tags=["Events"])

EventsResponse = List[Dict[str, Event]]


@event_router.get("/", response_model=EventsResponse)
async def retrieve_all_events(session=Depends(get_session)) -> EventsResponse:
    statement = select(Event)
    events = session.exec(statement).all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_single_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )


@event_router.post("/new")
async def create_event(new_event: Event = Body(...),
                       session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {"message": "Event created successfully."}


@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )


@event_router.delete("/")
async def delete_all_events(session=Depends(get_session)) -> dict:
    statement = select(Event)
    events = session.exec(statement).all()
    for event_row in events:
        event_dict = dict(event_row)
        event = session.get(Event, event_dict["Event"].id)
        session.delete(event)

    session.commit()

    return {"message": "Events delete successfully."}


@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, new_event: EventUpdate,
                       session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_event.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)

        return event
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {id} not found."
        )
