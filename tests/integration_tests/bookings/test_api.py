async def test_get_bookings_me(authenticated_ac):
    response = await authenticated_ac.get("/bookings/me")
    data = response.json()
    print(f"{data=}")
    assert response.status_code == 200


async def test_add_booking(db, authenticated_ac):
    room = (await db.rooms.get_all())[0]
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room.id,
            "date_from": "2026-02-02",
            "date_to": "2026-02-07"
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "data" in data
