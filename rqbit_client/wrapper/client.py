from os import getenv, path
from typing import Any, AsyncGenerator

import httpx
from dotenv import load_dotenv

from .exceptions import RqbitHTTPError


class RqbitClient:
    """A client for interacting with the rqbit API."""

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        """Initialize the RqbitClient."""
        if base_url is None:
            load_dotenv()
            base_url = getenv("RQBIT_URL", "http://localhost:3030")
        self.base_url = base_url
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """Make a regular API request."""
        try:
            response = await self._client.request(method, path, **kwargs)
            response.raise_for_status()
            if response.status_code == 204:  # No Content
                return None
            if response.headers.get("content-type") == "application/json":
                return response.json()
            return response.content
        except httpx.HTTPStatusError as e:
            raise RqbitHTTPError(
                f"HTTP error: {e.response.status_code} - {e.response.text}",
                status_code=e.response.status_code,
            ) from e
        except httpx.RequestError as e:
            raise RqbitHTTPError(f"Request error: {e}", status_code=0) from e

    async def _stream_request(
        self, method: str, path: str, **kwargs
    ) -> AsyncGenerator[bytes, None]:
        """Make a streaming API request."""
        try:
            async with self._client.stream(method, path, **kwargs) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    yield chunk
        except httpx.HTTPStatusError as e:
            raise RqbitHTTPError(
                f"HTTP error: {e.response.status_code} - {e.response.text}",
                status_code=e.response.status_code,
            ) from e
        except httpx.RequestError as e:
            raise RqbitHTTPError(f"Request error: {e}", status_code=0) from e

    async def close(self):
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # General
    async def get_apis(self) -> dict[str, Any]:
        """list all available APIs."""
        return await self._request("GET", "/")

    async def get_global_stats(self) -> dict[str, Any]:
        """Get global session stats."""
        return await self._request("GET", "/stats")

    async def get_metrics(self) -> str:
        """Get Prometheus metrics."""
        content = await self._request("GET", "/metrics")
        return content.decode("utf-8")

    async def stream_logs(self) -> AsyncGenerator[bytes, None]:
        """Continuously stream logs."""
        async for chunk in self._stream_request("GET", "/stream_logs"):
            yield chunk

    async def set_rust_log(self, log_level: str) -> None:
        """Set RUST_LOG post-launch for debugging."""
        await self._request("POST", "/rust_log", content=log_level)

    # DHT
    async def get_dht_stats(self) -> dict[str, Any]:
        """Get DHT stats."""
        return await self._request("GET", "/dht/stats")

    async def get_dht_table(self) -> list[dict[str, Any]]:
        """Get DHT routing table."""
        return await self._request("GET", "/dht/table")

    # Torrents
    async def list_torrents(self) -> list[dict[str, Any]]:
        """list all torrents."""
        return await self._request("GET", "/torrents")

    async def get_torrents_playlist(self) -> str:
        """Get a playlist for all torrents for supported players."""
        content = await self._request("GET", "/torrents/playlist")
        return content.decode("utf-8")

    async def add_torrent(
        self, url_or_path: str, content: bytes | None = None
    ) -> dict[str, Any]:
        """Add a torrent from a magnet, HTTP URL, or local file."""
        if content:
            return await self._request("POST", "/torrents", content=content)
        if path.exists(url_or_path):
            with open(url_or_path, "rb") as f:
                return await self._request("POST", "/torrents", content=f.read())
        return await self._request("POST", "/torrents", content=url_or_path)

    async def create_torrent(self, folder_path: str) -> dict[str, Any]:
        """Create a torrent from a local folder and start seeding."""
        return await self._request("POST", "/torrents/create", content=folder_path)

    async def resolve_magnet(self, magnet_link: str) -> bytes:
        """Resolve a magnet link to torrent file bytes."""
        return await self._request(
            "POST", "/torrents/resolve_magnet", content=magnet_link
        )

    # Torrent specific
    async def get_torrent_details(self, id_or_infohash: str) -> dict[str, Any]:
        """Get details for a specific torrent."""
        return await self._request("GET", f"/torrents/{id_or_infohash}")

    async def get_torrent_stats(self, id_or_infohash: str) -> dict[str, Any]:
        """Get stats for a specific torrent."""
        return await self._request("GET", f"/torrents/{id_or_infohash}/stats/v1")

    async def get_torrent_haves(self, id_or_infohash: str) -> list[bool]:
        """Get the bitfield of have pieces for a torrent."""
        return await self._request("GET", f"/torrents/{id_or_infohash}/haves")

    async def get_torrent_metadata(self, id_or_infohash: str) -> bytes:
        """Download the .torrent file for a torrent."""
        return await self._request("GET", f"/torrents/{id_or_infohash}/metadata")

    async def get_torrent_playlist(self, id_or_infohash: str) -> str:
        """Get a playlist for a specific torrent."""
        content = await self._request("GET", f"/torrents/{id_or_infohash}/playlist")
        return content.decode("utf-8")

    async def stream_torrent_file(
        self, id_or_infohash: str, file_idx: int, range_header: str | None = None
    ) -> AsyncGenerator[bytes, None]:
        """Stream a file from a torrent."""
        headers = {"Range": range_header} if range_header else {}
        path = f"/torrents/{id_or_infohash}/stream/{file_idx}"
        async for chunk in self._stream_request("GET", path, headers=headers):
            yield chunk

    async def pause_torrent(self, id_or_infohash: str) -> None:
        """Pause a torrent."""
        await self._request("POST", f"/torrents/{id_or_infohash}/pause")

    async def start_torrent(self, id_or_infohash: str) -> None:
        """Start (resume) a torrent."""
        await self._request("POST", f"/torrents/{id_or_infohash}/start")

    async def forget_torrent(self, id_or_infohash: str) -> None:
        """Forget a torrent, keeping the files."""
        await self._request("POST", f"/torrents/{id_or_infohash}/forget")

    async def delete_torrent(self, id_or_infohash: str) -> None:
        """Delete a torrent and its files."""
        await self._request("POST", f"/torrents/{id_or_infohash}/delete")

    async def add_peers(self, id_or_infohash: str, peers: list[str]) -> None:
        """Add peers to a torrent."""
        content = "\n".join(peers)
        await self._request(
            "POST", f"/torrents/{id_or_infohash}/add_peers", content=content
        )

    async def update_only_files(
        self, id_or_infohash: str, file_indices: list[int]
    ) -> None:
        """Change the selection of files to download."""
        await self._request(
            "POST",
            f"/torrents/{id_or_infohash}/update_only_files",
            json={"only_files": file_indices},
        )

    # Peer stats
    async def get_peer_stats(self, id_or_infohash: str) -> list[dict[str, Any]]:
        """Get per-peer stats for a torrent."""
        return await self._request("GET", f"/torrents/{id_or_infohash}/peer_stats")

    async def get_peer_stats_prometheus(self, id_or_infohash: str) -> str:
        """Get per-peer stats in Prometheus format."""
        content = await self._request(
            "GET", f"/torrents/{id_or_infohash}/peer_stats/prometheus"
        )
        return content.decode("utf-8")
