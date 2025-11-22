async def test_post_facilities(ac):
    facility_data = {"title": "Караоке"}
    response = await ac.post("/facilities", json=facility_data)

    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Караоке"


async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200
    assert len(response.json()) == 1
