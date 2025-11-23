import pytest


async def test_get_bookings_me(authenticated_ac):
    response = await authenticated_ac.get("/bookings/me")
    assert response.status_code == 200


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-02-02", "2026-02-07", 200),
    (1, "2026-02-03", "2026-02-08", 200),
    (1, "2026-02-04", "2026-02-09", 200),
    (1, "2026-02-05", "2026-02-10", 200),
    (1, "2026-02-06", "2026-02-11", 200),
    (1, "2026-02-07", "2026-02-12", 500),
    (1, "2026-02-15", "2026-02-22", 200)
])
async def test_add_booking(
        room_id, date_from, date_to, status_code, db, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    data = response.json()

    assert response.status_code == status_code
    if response.status_code == 200:
        assert isinstance(data, dict)
        assert "data" in data
