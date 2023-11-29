from copy import copy
import httpx
import pytest

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
PAYLOAD = {
    "email": "testuser@packt.com",
    "username": "testusername",
    "password": "testpassword"
}


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    test_response = {
        "message": "User successfully registered!"
    }

    response = await default_client.post("user/signup", json=PAYLOAD, headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_sign_in_by_username(default_client: httpx.AsyncClient) -> None:
    payload = copy(PAYLOAD)
    headers = copy(HEADERS)
    payload["email"] = "undefined_data"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    response = await default_client.post("user/signin", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_sign_in_by_email(default_client: httpx.AsyncClient) -> None:
    payload = copy(PAYLOAD)
    headers = copy(HEADERS)
    payload["username"] = "undefined_data"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    response = await default_client.post("user/signin", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"
