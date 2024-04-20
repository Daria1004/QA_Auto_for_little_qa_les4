import pytest
import requests
from faker import Faker
from constant import HEADERS, BASE_URL

faker = Faker()

@pytest.fixture(scope='session')
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(f"{BASE_URL}/auth", headers=HEADERS, json={"username": "admin", "password": "password123"})
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session


@pytest.fixture(scope='session')
def booking_for_test(auth_session, booking_data):
    create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    booking_id = create_booking.json().get("bookingid")

    yield booking_id

    auth_session.delete(f"{BASE_URL}/booking/{booking_id}")


@pytest.fixture(scope='session')
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": faker.date(),
            "checkout": faker.date()
        },
        "additionalneeds": faker.text()
    }


@pytest.fixture(scope='function')
def update_partial_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name()
    }


@pytest.fixture(scope='function')
def update_full_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice":faker.random_int(min=50, max=500),
        "depositpaid": True,
        "bookingdates": {
            "checkin": faker.date(),
            "checkout": faker.date()
        },
        "additionalneeds": faker.text()
    }
