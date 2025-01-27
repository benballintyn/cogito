import pytest
from httpx import Request, Response

from cogito.utils.api_client import APIClient


class MockAPI(APIClient):
    def __init__(self):
        super().__init__(base_url="https://mockapi.test")


@pytest.mark.asyncio
async def test_get_request(mocker):
    # Mock the Response object with a Request instance
    request = Request("GET", "https://mockapi.test/test")
    mock_response = Response(200, request=request, json={"message": "success"})

    # Patch the AsyncClient.request method
    mocker.patch("httpx.AsyncClient.request", return_value=mock_response)

    api = MockAPI()
    response = await api.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


@pytest.mark.asyncio
async def test_post_request(mocker):
    # Mock the Response object with a Request instance
    request = Request("POST", "https://mockapi.test/test")
    mock_response = Response(201, request=request, json={"message": "created"})

    # Patch the AsyncClient.request method
    mocker.patch("httpx.AsyncClient.request", return_value=mock_response)

    api = MockAPI()
    response = await api.post("/test", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"message": "created"}


@pytest.mark.asyncio
async def test_rate_limiting(mocker):
    # Mock the Response object with a Request instance
    request = Request("GET", "https://mockapi.test/test1")
    mock_response = Response(200, request=request, json={"message": "rate_limit"})

    # Patch the AsyncClient.request method
    mocker.patch("httpx.AsyncClient.request", return_value=mock_response)

    api = MockAPI()
    api.rate_limit_delay = 1.0  # Set rate limiting for the test

    # Ensure rate limiting is respected
    response1 = await api.get("/test1")
    response2 = await api.get("/test2")
    assert response1.status_code == 200
    assert response2.status_code == 200


@pytest.mark.asyncio
async def test_http_error_handling(mocker):
    # Mock the Response object with an HTTP error
    request = Request("GET", "https://mockapi.test/test")
    mock_response = Response(404, request=request, json={"error": "not found"})

    # Patch the AsyncClient.request method
    mocker.patch("httpx.AsyncClient.request", return_value=mock_response)

    api = MockAPI()
    with pytest.raises(Exception, match="404"):
        await api.get("/test")


@pytest.mark.asyncio
async def test_request_error_handling(mocker):
    # Mock a RequestError being raised
    mocker.patch("httpx.AsyncClient.request", side_effect=Exception("Request failed"))

    api = MockAPI()
    with pytest.raises(Exception, match="Request failed"):
        await api.get("/test")
