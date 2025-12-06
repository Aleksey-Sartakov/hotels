import pytest


@pytest.mark.parametrize(
    "email, password, reg_status_code, login_status_code, wrong_login_status_code, me_status_code",
    [
        ("simple@mail.com", "1234", 200, 200, 401, 200),
        ("simple@mail.com", "1234", 409, 200, 401, 200),
        ("numeric1234@mail.com", "1234", 200, 200, 401, 200),
        ("special*!_'@mail.com", "1234", 200, 200, 401, 200),
        ("hard_pass@mail.com", "Qwer$y!_zxC", 200, 200, 401, 200),
        ("pass_special@mail.com", "!@#$%^&*()_-=+'~`|\\/.,", 200, 200, 401, 200),
        ("space_pass@mail.com", "1234", 200, 200, 401, 200),
        ("space mail@mail.com", "1234", 422, 422, 422, 401),
        ("without_dog_mail.com", "1234", 422, 422, 422, 401),
    ],
)
async def test_full_auth(
    email, password, reg_status_code, login_status_code, wrong_login_status_code, me_status_code, ac
):
    response = await ac.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == reg_status_code

    response = await ac.get("/auth/me")
    assert response.status_code == 401

    wrong_login_resp1 = await ac.post("/auth/login", json={"email": email, "password": "wrong_pass"})
    assert wrong_login_resp1.status_code == wrong_login_status_code

    wrong_login_resp2 = await ac.post("/auth/login", json={"email": "wrong_email@mail.com", "password": password})
    assert wrong_login_resp2.status_code == 401

    login_resp = await ac.post("/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == login_status_code

    me_resp = await ac.get("/auth/me")
    data = me_resp.json()
    assert me_resp.status_code == me_status_code
    if me_resp.status_code == 200:
        assert "id" in data
        assert "email" in data
        assert data["email"] == email

    response = await ac.post("/auth/logout")
    assert response.status_code == 200

    response = await ac.get("/auth/me")
    assert response.status_code == 401
