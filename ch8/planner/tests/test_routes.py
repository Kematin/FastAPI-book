import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event


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
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")
    response = response
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_get_single_event(default_client: httpx.AsyncClient, mock_event: Event,
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
