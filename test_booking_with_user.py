import pytest

from conftest import faker, booking_hp
from constant import BASE_URL


def test_create_and_delete_booking(auth_session):
    booking_user = booking_hp()
    create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_user)
    assert create_booking.status_code == 200, "Бронь не найдена"

    booking_id = create_booking.json().get("bookingid")  # извлекаем id
    assert booking_id is not None, "Индентификатор брони не найден в ответе"
    print(create_booking.json())

    delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
    assert delete_booking.status_code == 201, "Бронь не найдена"

    get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert get_booking.status_code == 404, "Передан существующий id"


def test_get_booking_by_name(auth_session, create_harry_potter_id):
    # ищем бронирования по фамилии
    get_booking = auth_session.get(f"{BASE_URL}/booking?lastname=Potter")
    assert len(get_booking.json()) > 0, "Бронирования на такую фамилию не найдены"
    print(get_booking.json())

def update_partial_data():
    return {
        "firstname": "James",
        "lastname": faker.last_name()
    }

def test_partial_update_booking(auth_session, create_harry_potter_id):
    update_partial_user = update_partial_data()
    booking_old = auth_session.get(f"{BASE_URL}/booking/{create_harry_potter_id}")
    booking_upd_part = auth_session.patch(f"{BASE_URL}/booking/{create_harry_potter_id}", json=update_partial_user)
    assert (update_partial_user['firstname'] == booking_upd_part.json().get('firstname')
            and update_partial_user['lastname'] == booking_upd_part.json().get('lastname'))
    assert not booking_old.json().get('firstname') == booking_upd_part.json().get('firstname')
    print(booking_upd_part.json())


def update_full_data():
    return {
        "firstname": "Ron",
        "lastname": "Weasley",
        "totalprice": 1010,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }


def test_full_update_booking(auth_session, create_harry_potter_id):
    update_full_user = update_full_data()
    booking_upd_full = auth_session.put(f"{BASE_URL}/booking/{create_harry_potter_id}", json=update_full_user)
    assert update_full_user['totalprice'] == booking_upd_full.json().get('totalprice')
    print(booking_upd_full.json())


def test_get_booking_non_existent_id(auth_session):
    booking_id = 99999
    get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert get_booking.status_code == 404, "Передан существующий id"
    print(get_booking.status_code)
