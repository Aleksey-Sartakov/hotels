async def test_get_bookings_me(authenticated_ac):
    response = await authenticated_ac.get("/bookings/me")
    data = response.json()
    print(f"{data=}")
    assert response.status_code == 200
