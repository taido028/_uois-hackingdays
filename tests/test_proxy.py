# import os
# import pytest
# from httpx import AsyncClient
# from fastapi import FastAPI
# import asyncio
# from unittest.mock import mock_open, patch
# from server.gqlproxy import connectProxy, Item  

# @pytest.fixture
# def app():
#     app = FastAPI()
#     connectProxy(app)
#     return app

# @pytest.fixture
# def client(app):
#     return AsyncClient(app=app, base_url="http://test")

# from unittest.mock import patch

# @pytest.mark.asyncio
# async def test_apigql_get(client):
#     with patch('os.path.exists', return_value=True), \
#          patch('builtins.open', mock_open(read_data="data")):
#         response = await client.get("/gql")
#         assert response.status_code == 200
#         assert response.content == b'data'


# @pytest.mark.asyncio
# async def test_apidoc_get(client):
#     with patch('os.path.realpath', return_value='/path/to/voyager.html'):
#         response = await client.get("/doc")
#         assert response.status_code == 200
#         assert response.content == b'/path/to/voyager.html'

# @pytest.mark.asyncio
# async def test_apigql_post(client):
#     item = {"query": "{ users { id name } }", "variables": None, "operationName": None}
#     headers = {"authorization": "Bearer some_token"}

#     with patch('aiohttp.ClientSession.post') as mock_post:
#         mock_post.return_value.__aenter__.return_value.status = 200
#         mock_post.return_value.__aenter__.return_value.json = asyncio.coroutine(lambda: {"data": {"users": [{"id": "1", "name": "John Doe"}]}})
        
#         response = await client.post("/gql", json=item, headers=headers)
#         assert response.status_code == 200
#         assert response.json() == {"data": {"users": [{"id": "1", "name": "John Doe"}]}}

