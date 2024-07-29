import logging
import uuid
from fastapi.testclient import TestClient
import pytest

logging.basicConfig(level=logging.DEBUG)


def register_user(client: TestClient, username: str, password: str, first_name: str, last_name: str, email: str):
    response = client.post('/users/signup',
                           json={"username": username,
                                 "password": password,
                                 "first_name": first_name,
                                 "last_name": last_name,
                                 "email": email})
    return response


def login_user(client: TestClient, username: str, password: str):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
    }
    login_response = client.post('/users/signin', headers=headers, data=data)
    assert login_response.status_code == 200
    return login_response


def test_home_request(client: TestClient):
    response = client.get('/test')
    assert response.status_code == 200
    assert response.json() == {'message': 'success'}


def test_register(client: TestClient):
    response = register_user(client, "kasha666", "kasha", "Test", "User", "sashhakudashha666@gmail.com")
    assert response.status_code == 200
    assert response.json()['username'] == 'kasha666'


def test_login(client: TestClient):
    login_response = login_user(client, "kasha@gmail.com", "kasha")
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_request(client: TestClient):
    response = client.post('/users/handle_request',
                           params={"data": "2024-01-01", "model": "prophet_model"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['message'] == 'Task sent to worker'


def test_balance(client: TestClient):
    response = client.get('/balances/balance')
    assert response.status_code == 200
    assert 'amount' in response.json()


def test_add_balance(client: TestClient):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {'amount': 0.0}
    response = client.post(
        "/balances/add_balance", headers=headers, data=data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    response_json = response.json()
    assert "amount" in response_json, "Response JSON does not contain 'amount'"
    assert response_json["amount"] == 400.0, f"Expected amount 100.0 but got {response_json['amount']}"


def test_invalid_email(client: TestClient):
    response = register_user(client, "kas44444ha", "ka44444sha", "Tes44444t", "U4444", "invalidkasha999999")
    assert response.status_code == 422
    logging.debug(response.status_code)
    assert 'detail' in response.json()


def test_invalid_date(client: TestClient):
    login_response = login_user(client, "kasha@gmail.com", "kasha")
    access_token = login_response.json()["access_token"]
    response = client.post('/users/handle_request',
                           headers={"Authorization": f"Bearer {access_token}"},
                           json={"data": "invalid-date", "model": "prophet_model"})
    logging.debug(f"Invalid date request response: {response.json()}")

    assert response.status_code == 422
    assert 'detail' in response.json()


