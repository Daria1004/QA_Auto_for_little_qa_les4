from constant import BASE_URL


def test_create_and_delete_booking(auth_session, booking_data):
    create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    assert create_booking.status_code == 200, "Ошибка при создании брони"
    assert create_booking.status_code == 200, "Бронь не найдена"
    assert create_booking.json()["booking"]['firstname'] == booking_data['firstname'], "Заданное имя не совпадает"
    assert create_booking.json()["booking"]['lastname'] == booking_data['lastname'], "Заданная фамилия не совпадает"
    assert create_booking.json()["booking"]['totalprice'] == booking_data['totalprice'], "Заданная стоимость не совпадает"
    assert create_booking.json()["booking"]['bookingdates']['checkin'] == booking_data['bookingdates']['checkin'], "Заданная дата заселения не совпадает"
    assert create_booking.json()["booking"]['bookingdates']['checkout'] == booking_data['bookingdates']['checkout'], "Заданная дата выселения не совпадает"
    assert create_booking.json()["booking"]['additionalneeds'] == booking_data['additionalneeds'], "Заданный комментарий не совпадает"

    booking_id = create_booking.json().get("bookingid")
    assert booking_id is not None, "Индентификатор брони не найден в ответе"

    get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert get_booking.status_code == 200, "Бронь не найдена"
    assert get_booking.json()['firstname'] == booking_data['firstname'], "Заданное имя не совпадает"
    assert get_booking.json()['lastname'] == booking_data['lastname'], "Заданная фамилия не совпадает"
    assert get_booking.json()['totalprice'] == booking_data['totalprice'], "Заданная стоимость не совпадает"
    assert get_booking.json()['bookingdates']['checkin'] == booking_data['bookingdates']['checkin'], "Заданная дата заселения не совпадает"
    assert get_booking.json()['bookingdates']['checkout'] == booking_data['bookingdates']['checkout'], "Заданная дата выселения не совпадает"
    assert get_booking.json()['additionalneeds'] == booking_data['additionalneeds'], "Заданный комментарий не совпадает"

    delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
    assert delete_booking.status_code == 201, "Бронь не найдена"

    get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert get_booking.status_code == 404, "Передан существующий id"


def test_get_booking_by_filter(auth_session, booking_for_test, booking_data):
    get_booking = auth_session.get(f"{BASE_URL}/booking?firstname={booking_data['firstname']}")
    assert get_booking.status_code == 200, "Бронь не найдена"
    assert len(get_booking.json()) > 0, "Бронирования на такое имя не найдены"
    ids = [book['bookingid'] for book in get_booking.json()]
    assert booking_for_test in ids
    get_booking = auth_session.get(f"{BASE_URL}/booking?lastname={booking_data['lastname']}")
    assert get_booking.status_code == 200, "Бронь не найдена"
    assert len(get_booking.json()) > 0, "Бронирования на такую фамилию не найдены"
    ids = [book['bookingid'] for book in get_booking.json()]
    assert booking_for_test in ids
    get_booking = auth_session.get(f"{BASE_URL}/booking?additionalneeds={booking_data['additionalneeds']}")
    assert get_booking.status_code == 200, "Бронь не найдена"
    assert len(get_booking.json()) > 0, "Бронирования с таким комментарием не найдены"
    ids = [book['bookingid'] for book in get_booking.json()]
    assert booking_for_test in ids


def test_partial_update_booking(auth_session, booking_for_test, update_partial_data):
    booking_old = auth_session.get(f"{BASE_URL}/booking/{booking_for_test}")
    booking_upd_part = auth_session.patch(f"{BASE_URL}/booking/{booking_for_test}", json=update_partial_data)
    assert (update_partial_data['firstname'] == booking_upd_part.json().get('firstname')
            and update_partial_data['lastname'] == booking_upd_part.json().get('lastname'))
    assert not booking_old.json().get('firstname') == booking_upd_part.json().get('firstname')


def test_full_update_booking(auth_session, booking_for_test, update_full_data):
    booking_upd_full = auth_session.put(f"{BASE_URL}/booking/{booking_for_test}", json=update_full_data)
    assert update_full_data['totalprice'] == booking_upd_full.json().get('totalprice')


def test_get_booking_non_existent_id(auth_session):
    booking_id = 99999
    get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert get_booking.status_code == 404, "Передан существующий id"
