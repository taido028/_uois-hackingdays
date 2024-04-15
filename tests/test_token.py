import pytest
import logging
import jwt

@pytest.mark.asyncio
async def test_publickey(DemoFalse, FastAPIClient, Publickey):
    # logging.info(f"AccessToken is {AccessToken}")
    logging.info(f"Publickey is {Publickey}")
    # response = FastAPIClient.post("/gql", headers=headers, json=json)



@pytest.mark.asyncio
async def test_admintoken(DemoFalse, Publickey, AdminToken):
    # logging.info(f"AccessToken is {AccessToken}")
    logging.info(f"Publickey is {Publickey}")
    key = Publickey.replace('"', '').replace('\\n', '\n').encode("ascii")
    logging.info(f"AdminToken is {AdminToken}")
    # response = FastAPIClient.post("/gql", headers=headers, json=json)
    decodedjwt = jwt.decode(jwt=AdminToken, key=key, algorithms=["RS256"])
    logging.info(f"jwt is {decodedjwt}")
    userid = decodedjwt["user_id"]
    logging.info(f"userid is {userid}")


@pytest.mark.asyncio
async def test_app_index(DemoFalse, FastAPIClient):
    # logging.info(f"AccessToken is {AccessToken}")
    response = FastAPIClient.get("/")
    assert response.status_code == 200

# pytest --cov-report term-missing --cov=server tests --log-cli-level=INFO -x
    
import pytest
from unittest.mock import AsyncMock, patch
from starlette.authentication import AuthenticationError
from server.authenticationMiddleware import BasicAuthBackend
import jwt


@pytest.mark.asyncio
async def test_get_public_key_success():
    backend = BasicAuthBackend()
    # Giả lập thành công khi lấy public key
    with patch('aiohttp.ClientSession.get') as mocked_get:
        mocked_response = AsyncMock(status=200, text=AsyncMock(return_value='"valid_key"\\n'))
        mocked_get.return_value.__aenter__.return_value = mocked_response
        public_key = await backend.getPublicKey()
        assert public_key == b'valid_key\n'
        assert backend.publickey == b'valid_key\n'

@pytest.mark.asyncio
async def test_get_public_key_failure():
    backend = BasicAuthBackend()
    # Giả lập thất bại khi lấy public key
    with patch('aiohttp.ClientSession.get') as mocked_get:
        mocked_response = AsyncMock(status=404)
        mocked_get.return_value.__aenter__.return_value = mocked_response
        with pytest.raises(AuthenticationError):
            await backend.getPublicKey()


@pytest.mark.asyncio
async def test_authenticate_success():
    backend = BasicAuthBackend()
    valid_key = b"valid_key\n"
    backend.publickey = valid_key
    jwt_encoded = jwt.encode({"user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}, valid_key, algorithm="HS256")
    conn = AsyncMock(headers={"Authorization": f"Bearer {jwt_encoded}"}, cookies={})

    with patch('jwt.decode', return_value={"user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}):
        credentials, user = await backend.authenticate(conn)  
        assert credentials.scopes == ["authenticated"]
        assert user["id"] == "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"


# @pytest.mark.asyncio
# async def test_authenticate_invalid_token():
#     # Tạo đối tượng backend
#     backend = BasicAuthBackend()
#     backend.publickey = b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMmQ5ZGM1Y2EtYTRhMi0xMWVkLWI5ZGYtMDI0MmFjMTIwMDAzIn0.XJQz5ISKRhwQ8wx_UDnflk9T4kxZi6OIqmRex4_ePv4' 

#    
#     jwt_encoded = jwt.encode(
#         {"user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
#         "d63d503bebb907636e0a35b70d446f73d4d820889e441fac82e16919621cdfe2",
#         algorithm="HS256"
#     )
    
#     conn = AsyncMock()
#     conn.headers = {"Authorization": f"Bearer {jwt_encoded}"}
#     conn.cookies = {}

#     
#     with pytest.raises(AuthenticationError) as exc_info:
#         await backend.authenticate(conn)
#     assert "Invalid signature" in str(exc_info.value), "The error should specifically mention the invalid signature"



@pytest.mark.asyncio
async def test_authenticate_missing_token():
    backend = BasicAuthBackend()
    conn = AsyncMock(headers={}, cookies={})
    
    with pytest.raises(AuthenticationError, match="missing code"):
        await backend.authenticate(conn)


import pytest
from starlette.responses import RedirectResponse, PlainTextResponse
from starlette.requests import Request
from http import HTTPStatus
from starlette.datastructures import URL
from server.authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthenticationMiddleware404  
from unittest.mock import Mock

from http import HTTPStatus
from starlette.responses import RedirectResponse, PlainTextResponse
from starlette.requests import Request
import pytest

@pytest.mark.asyncio
async def test_basic_authentication_middleware_302():
    # Tạo một request giả lập
    request = Request(scope={"type": "http", "path": "/some/path", "headers": []})
    # Tạo một exception giả
    exception = Exception("Test exception")

    # Gọi phương thức default_on_error
    response = BasicAuthenticationMiddleware302.default_on_error(request, exception)

    # Kiểm tra liệu response có đúng là RedirectResponse không    
    assert isinstance(response, RedirectResponse)
    # Kiểm tra status code của response
    assert response.status_code == HTTPStatus.FOUND  # 302 FOUND  
    # Kiểm tra URL đích của redirect
    assert response.headers["location"] == "/oauth/login2?redirect_uri=/some/path"

@pytest.mark.asyncio
async def test_basic_authentication_middleware_404():
    # Tạo một request giả lập
    request = Request(scope={"type": "http", "path": "/some/path", "headers": []})
    # Tạo một exception giả
    exception = Exception("Test exception")

    # Gọi phương thức default_on_error
    response = BasicAuthenticationMiddleware404.default_on_error(request, exception)

    # Kiểm tra liệu response có đúng là PlainTextResponse không   
    assert isinstance(response, PlainTextResponse)
    # Kiểm tra status code của response
    assert response.status_code == HTTPStatus.NOT_FOUND  # 404 Not Found
    # Kiểm tra nội dung của response
    assert response.body.decode() == "Unauthorized for /some/path"




