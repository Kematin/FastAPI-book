import httpx
import pytest


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "email": "testuser@packt.com",
        "username": "testusername",
        "password": "testpassword"
    }

    test_response = {
        "message": "User successfully registered!"
    }

    response = await default_client.post("user/signup", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_sign_in_by_username(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testusername",
        "password": "testpassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = await default_client.post("user/signin", data=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_sign_in_by_email(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuser@packt.com",
        "password": "testpassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = await default_client.post("user/signin", data=payload, headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_sign_with_wrong_credentials(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "wrong_username",
        "password": "testpassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = await default_client.post("user/signin", data=payload, headers=headers)
    print(response.json())
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_sign_with_wrong_password(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testusername",
        "password": "wrongpassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = await default_client.post("user/signin", data=payload, headers=headers)
    print(response.json())
    assert response.status_code == 403
