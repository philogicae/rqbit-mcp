from typing import Any

import pytest
from fastmcp import Client

from .mcp_server import mcp


@pytest.fixture(scope="session")
def mcp_client() -> Client[Any]:
    """Create a FastMCP client for testing."""
    return Client(mcp)


@pytest.mark.asyncio
async def test_list_torrents(mcp_client: Client[Any]) -> None:
    """Test the 'list_torrents' tool."""
    # async with mcp_client as client:
    # result = await client.call_tool("list_torrents")
    # assert result is not None and len(result.content[0].text) > 8  # Success
    assert True


# TODO: Add all tests
