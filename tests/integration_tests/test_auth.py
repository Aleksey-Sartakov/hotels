from src.services.auth import AuthService


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    auth_service = AuthService()
    jwt_token = auth_service.create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = auth_service.decode_token(jwt_token)

    assert payload
    assert payload["user_id"] == data["user_id"]
