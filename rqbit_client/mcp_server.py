import logging
from json import dumps
from typing import Any

from fastmcp import FastMCP

from .wrapper import RqbitClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RqbitMCP")

mcp: FastMCP[Any] = FastMCP("Rqbit")

rqbit_client = RqbitClient()


@mcp.tool()
async def list_torrents() -> str:
    """List all torrents."""
    logger.info("Listing all torrents")
    result = await rqbit_client.list_torrents()
    if isinstance(result, str):
        logger.error(f"Error listing torrents: {result}")
        return f"Error listing torrents: {result}"
    return dumps(result)


@mcp.tool()
async def download_torrent(magnet_link_or_url_or_path: str) -> str:
    """Download a torrent from a magnet link, HTTP URL, or local file."""
    logger.info(
        f"Downloading torrent from magnet link/HTTP URL/local file: {magnet_link_or_url_or_path}"
    )
    result = await rqbit_client.add_torrent(magnet_link_or_url_or_path)
    if isinstance(result, str):
        error = f"Error downloading torrent {magnet_link_or_url_or_path}: {result}"
        logger.error(error)
        return error
    return dumps(result)


@mcp.tool()
async def get_torrent_details(torrent_id: str) -> str:
    """Get details for a specific torrent by its ID or infohash."""
    logger.info(f"Getting details for torrent: {torrent_id}")
    result = await rqbit_client.get_torrent_details(torrent_id)
    if isinstance(result, str):
        error = f"Error getting torrent details {torrent_id}: {result}"
        logger.error(error)
        return error
    return dumps(result)


@mcp.tool()
async def get_torrent_stats(torrent_id: str) -> str:
    """Get stats and status for a specific torrent by its ID or infohash."""
    logger.info(f"Getting stats/status for torrent: {torrent_id}")
    result = await rqbit_client.get_torrent_stats(torrent_id)
    if isinstance(result, str):
        error = f"Error getting torrent stats {torrent_id}: {result}"
        logger.error(error)
        return error
    return dumps(result)


@mcp.tool()
async def delete_torrent(torrent_id: str) -> str:
    """Delete a torrent and its files."""
    logger.info(f"Deleting torrent: {torrent_id}")
    result = await rqbit_client.delete_torrent(torrent_id)
    if isinstance(result, str):
        error = f"Error deleting torrent {torrent_id}: {result}"
        logger.error(error)
        return error
    return "Successfully deleted torrent " + torrent_id


@mcp.tool()
async def start_torrent(torrent_id: str) -> str:
    """Start (resume) a torrent."""
    logger.info(f"Starting torrent: {torrent_id}")
    result = await rqbit_client.start_torrent(torrent_id)
    if isinstance(result, str):
        error = f"Error starting torrent {torrent_id}: {result}"
        logger.error(error)
        return error
    return "Successfully started torrent " + torrent_id


@mcp.tool()
async def pause_torrent(torrent_id: str) -> str:
    """Pause a torrent."""
    logger.info(f"Pausing torrent: {torrent_id}")
    result = await rqbit_client.pause_torrent(torrent_id)
    if isinstance(result, str):
        error = f"Error pausing torrent {torrent_id}: {result}"
        logger.error(error)
        return error
    return "Successfully paused torrent " + torrent_id


@mcp.tool()
async def forget_torrent(torrent_id: str) -> str:
    """Forget a torrent, keeping the files."""
    logger.info(f"Forgetting torrent: {torrent_id}")
    result = await rqbit_client.forget_torrent(torrent_id)
    if isinstance(result, str):
        error = f"Error forgetting torrent {torrent_id}: {result}"
        logger.error(error)
        return error
    return "Successfully forgot torrent " + torrent_id
