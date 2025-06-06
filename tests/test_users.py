import pytest
from httpx import AsyncClient
from jose import jwt


# =========== Tests for User Creation ===========

# Tests for succesful User Creation
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = await client.post("/api/users/", json=user_data)
    print(response.json())
    assert response.status_code == 201
    
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data 
    
@pytest.mark.asyncio
async  def test_create_user_with_invalid_email(client: AsyncClient):
    user_data = {
        "username": "testuser2",
        "email": "invalid-email",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = await client.post("/api/users/", json=user_data)
    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_create_user_with_short_password(client: AsyncClient):
    user_data = {
        "username": "testuser3",
        "email": "testuser3@example.com",
        "password": "short",
        "first_name": "Test",
        "last_name": "User"
    }
    response = await client.post("/api/users/", json=user_data)
    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_create_user_with_non_alphanumeric_username(client: AsyncClient):
    user_data = {
        "username": "test_user4",
        "email": "testuser4@example.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    response = await client.post("/api/users/", json=user_data)
    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_create_user_with_existing_username(client: AsyncClient):
    user_data = {
        "username": "testuser",
        "email": "testuser5@example.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    response = await client.post("/api/users/", json=user_data)
    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_create_user_with_existing_email(client: AsyncClient):
    user_data = {
        "username": "testuser6",
        "email": "testuser@example.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    response = await client.post("/api/users/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_with_missing_fields(client: AsyncClient):
    user_data = {
        "username": "testuser7",
        "email": "testuser7@example.com",
        "password": "Test@1234",
        # missing first_name
        "last_name": "User"
    }
    response = await client.post("/api/users/", json=user_data)
    assert response.status_code == 422
    
# =========== Tests for User Retrieval ===========
@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    # First, create a user to retrieve
    user_data = {
        "username": "testuser8",
        "email": "testuser8@example.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    
    await client.post("/api/users/", json=user_data)
    
    login_data = {
        "username": "testuser8",
        "password": "Test@1234"
    }
    
    login_response = await client.post("/api/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("api/users/me", headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

@pytest.mark.asyncio
async def test_get_user_unauthorized(client: AsyncClient):
    response = await client.get("api/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    
@pytest.mark.asyncio
async def test_get_user_modified_tokken(client: AsyncClient):
    fake_secret = "wrongsecret"
    payload = {"sub": "1"}
    fake_token = jwt.encode(payload, fake_secret, algorithm="HS256")

    headers = {"Authorization": f"Bearer {fake_token}"}
    
    response = await client.get("api/users/me", headers=headers)
    assert response.status_code == 401
    
# =========== Tests for User Update ===========
@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    # First, create a user to update
    user_data = {
        "username": "testuser9",
        "email": "testuser9@example.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    await client.post("/api/users/", json=user_data)
    login_data = {
        "username": "testuser9",
        "password": "Test@1234"
    }
    
    login_response = await client.post("/api/login", data=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "username": "updateduser9",
        "first_name": "Updated",
        "last_name": "Successfully",
        "password": "NewPassword@1234"
    }
    response = await client.put("api/users/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == update_data["username"]
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    
@pytest.mark.asyncio
async def test_update_user_unauthorized(client: AsyncClient):
    update_data = {
        "username": "updateduser10",
        "first_name": "Updated",
        "last_name": "Successfully",
        "password": "NewPassword@1234"
    }
    response = await client.put("api/users/me", json=update_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    
@pytest.mark.asyncio
async def test_update_user_invalid_token(client: AsyncClient):
    fake_secret = "wrongsecret"
    payload = {"sub": "1"}
    fake_token = jwt.encode(payload, fake_secret, algorithm="HS256")

    headers = {"Authorization": f"Bearer {fake_token}"}
    update_data = {
        "username": "updateduser11",
        "first_name": "Updated",
        "last_name": "Successfully",
        "password": "NewPassword@1234"
    }
    response = await client.put("api/users/me", json=update_data, headers=headers)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_user_with_duplicated_username(client: AsyncClient):
    user_data = {
        "username": "testuser12",
        "email": "testuser12@gmail.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    await client.post("/api/users/", json=user_data)
    
    user_data2 = {
        "username": "testuser13",
        "email": "testuser13@example.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User"
    }
    await client.post("/api/users/", json=user_data2)
    
    login_data = {
        "username": "testuser12",
        "password": "Test@1234"
    }
    login_response = await client.post("/api/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "username": "testuser13"
    }
    response = await client.put("api/users/me", json=update_data, headers=headers)
    print(response.json())
    assert response.status_code == 422
    