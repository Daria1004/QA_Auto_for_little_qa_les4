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

    session.headers.update({"Cookie": f"token={token}"})  # извлекаем токен
    return session


@pytest.fixture()
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-10",
            "checkout": "2019-04-13"
        },
        "additionalneeds": "Breakfast"
    }


@pytest.fixture
def create_harry_potter_id(auth_session):
    booking_user = booking_hp()
    create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_user)
    booking_id = create_booking.json().get("bookingid")  # извлекаем id
    yield booking_id
    auth_session.delete(f"{BASE_URL}/booking/{booking_id}")


def booking_hp():
    return {
        "firstname": "Harry",
        "lastname": 'Potter',
        "totalprice": 100500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-13",
            "checkout": "2019-04-15"
        },
        "additionalneeds": "Breakfast in the pool"
    }
