async def test_post_facilities(ac):
    facility_data = {"title": "Караоке"}
    response = await ac.post("/facilities", json=facility_data)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "data" in data
    assert data["data"]["title"] == "Караоке"


async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
