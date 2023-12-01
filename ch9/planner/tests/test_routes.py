import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event

client = httpx.AsyncClient


@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("testuser@packt.com")


@pytest.fixture(scope="module")
async def mock_event() -> Event:
    data = {
        "creator": "testuser@packt.com",
        "title": "FastAPI book launch test",
        "image_url": "https://site.com/image.png",
        "description": "content about fastapi",
        "tags": ["python", "web", "rest"],
        "location": "Google meet"
    }
    new_event = Event(**data)
    await Event.insert_one(new_event)
    yield new_event


@pytest.mark.asyncio
async def test_get_events(default_client: client, mock_event: Event) -> None:
    response = await default_client.get("/event/")
    response = response
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_get_single_event(default_client: client, mock_event: Event,
                                access_token: str) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url=url, headers=headers)

    assert response.status_code == 200
    assert response.json()["_id"] == str(mock_event.id)
    assert response.json()["creator"] == mock_event.creator


@pytest.mark.asyncio
async def test_post_event(default_client: client, access_token: str) -> None:
    payload = {
        "title": "Django book v2",
        "image_url": "https://site.com/image.png",
        "description": "content about drf",
        "tags": ["python", "web", "rest", "django", "drf"],
        "location": "Google meet"
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    test_response = {
        "message": "Event created successfully."
    }

    response = await default_client.post("/event/new", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_events_count(default_client: client) -> None:
    response = await default_client.get("/event/")

    events = response.json()

    assert response.status_code == 200
    assert len(events) == 2


@pytest.mark.asyncio
async def test_update_event(default_client: client, mock_event: Event,
                            access_token: str) -> None:
    url = f"/event/edit/{mock_event.id}"
    payload = {
        "title": "FastAPI book V2 launch test",
        "location": "Amazon meet"
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = await default_client.put(url, json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "FastAPI book V2 launch test"
    assert response.json()["location"] == "Amazon meet"


@pytest.mark.asyncio
async def test_delete_event(default_client: client, mock_event: Event,
                            access_token: str) -> None:
    url = f"/event/{mock_event.id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {
        "message": "Event deleted successfully."
    }

    response = await default_client.delete(url, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response

    response = await default_client.get(f"/event/{mock_event.id}", headers=headers)
    assert response.status_code == 404
