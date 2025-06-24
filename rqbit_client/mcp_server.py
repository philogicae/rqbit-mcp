import logging
from typing import Any

from fastmcp import FastMCP

from .wrapper import RqbitClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RqbitMCP")

mcp: FastMCP[Any] = FastMCP("RqbitClient")

rqbit_client = RqbitClient()


@mcp.tool()
async def list_torrents() -> list[dict[str, Any]]:
    """List all torrents."""
    logger.info("Listing all torrents")
    return await rqbit_client.list_torrents()


@mcp.tool()
async def add_torrent(magnet_link: str) -> dict[str, Any]:
    """Add a torrent from a magnet link."""
    logger.info(f"Adding torrent from magnet link: {magnet_link}")
    return await rqbit_client.add_torrent(magnet_link)


@mcp.tool()
async def get_torrent_details(torrent_id: str) -> dict[str, Any]:
    """Get details for a specific torrent by its ID or infohash."""
    logger.info(f"Getting details for torrent: {torrent_id}")
    return await rqbit_client.get_torrent_details(torrent_id)


@mcp.tool()
async def get_torrent_stats(torrent_id: str) -> dict[str, Any]:
    """Get stats and status for a specific torrent by its ID or infohash."""
    logger.info(f"Getting stats/status for torrent: {torrent_id}")
    return await rqbit_client.get_torrent_stats(torrent_id)


@mcp.tool()
async def delete_torrent(torrent_id: str) -> None:
    """Delete a torrent and its files."""
    logger.info(f"Deleting torrent: {torrent_id}")
    await rqbit_client.delete_torrent(torrent_id)


@mcp.tool()
async def start_torrent(torrent_id: str) -> None:
    """Start (resume) a torrent."""
    logger.info(f"Starting torrent: {torrent_id}")
    await rqbit_client.start_torrent(torrent_id)


@mcp.tool()
async def pause_torrent(torrent_id: str) -> None:
    """Pause a torrent."""
    logger.info(f"Pausing torrent: {torrent_id}")
    await rqbit_client.pause_torrent(torrent_id)


@mcp.tool()
async def forget_torrent(torrent_id: str) -> None:
    """Forget a torrent, keeping the files."""
    logger.info(f"Forgetting torrent: {torrent_id}")
    await rqbit_client.forget_torrent(torrent_id)
