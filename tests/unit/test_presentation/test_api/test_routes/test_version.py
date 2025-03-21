import fastapi


async def test_get_version(mocked_api_client):
    response = await mocked_api_client.get("/version")

    assert response.status_code == fastapi.status.HTTP_200_OK
