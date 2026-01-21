import pytest


@pytest.mark.asyncio
async def test_get_organization_by_id():
    response = api_client.get("v1/organizations/1")
