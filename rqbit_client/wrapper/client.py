import os
from base64 import b64encode
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
            base_url = os.getenv("RQBIT_URL", "http://localhost:3030")
        self.base_url = base_url
        headers = {}
        basic_auth = os.getenv("RQBIT_HTTP_BASIC_AUTH_USERPASS")
        if basic_auth:
            auth_bytes = basic_auth.encode("ascii")
            auth_base64 = b64encode(auth_bytes).decode("ascii")
            headers["Authorization"] = f"Basic {auth_base64}"

        self._client = httpx.AsyncClient(
            base_url=base_url, timeout=timeout, headers=headers
        )

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """Make a regular API request."""
        try:
            response = await self._client.request(method, path, **kwargs)
            response.raise_for_status()
            if response.status_code == 204:  # No Content
                return None
            if response.headers.get("content-type") == "application/json":
                return response.json()
            if response.headers.get("content-type") == "application/octet-stream":
                return await response.read()  # type: ignore
            return response.text
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

    async def _safe_request(self, method: str, path: str, **kwargs) -> Any | str | None:
        try:
            return await self._request(method, path, **kwargs)
        except RqbitHTTPError as e:
            return str(e)

    async def _safe_stream_request(
        self, method: str, path: str, **kwargs
    ) -> AsyncGenerator[bytes, None] | str:
        try:
            async for chunk in self._stream_request(method, path, **kwargs):
                yield chunk
        except RqbitHTTPError as e:
            yield str(e).encode("utf-8")

    # General
    async def get_apis(self) -> dict[str, Any] | str:
        """list all available APIs."""
        return await self._safe_request("GET", "/")  # type: ignore

    async def get_global_stats(self) -> dict[str, Any] | str:
        """Get global session stats."""
        return await self._safe_request("GET", "/stats")  # type: ignore

    async def get_metrics(self) -> str:
        """Get Prometheus metrics."""
        content = await self._safe_request("GET", "/metrics")
        if isinstance(content, str):
            return content
        return content  # type: ignore

    async def stream_logs(self) -> AsyncGenerator[bytes, None] | str:
        """Continuously stream logs."""
        async for chunk in self._safe_stream_request("GET", "/stream_logs"):  # type: ignore
            yield chunk  # type: ignore

    async def set_rust_log(self, log_level: str) -> None | str:
        """Set RUST_LOG post-launch for debugging."""
        return await self._safe_request("POST", "/rust_log", content=log_level)

    # DHT
    async def get_dht_stats(self) -> dict[str, Any] | str:
        """Get DHT stats."""
        return await self._safe_request("GET", "/dht/stats")  # type: ignore

    async def get_dht_table(self) -> list[dict[str, Any]] | str:
        """Get DHT routing table."""
        return await self._safe_request("GET", "/dht/table")  # type: ignore

    # Torrents
    async def list_torrents(self) -> list[dict[str, Any]] | str:
        """list all torrents."""
        return await self._safe_request("GET", "/torrents")  # type: ignore

    async def get_torrents_playlist(self) -> str:
        """Get a playlist for all torrents for supported players."""
        content = await self._safe_request("GET", "/torrents/playlist")
        if isinstance(content, str):
            return content
        return content  # type: ignore

    async def add_torrent(
        self, url_or_path: str, content: bytes | None = None
    ) -> dict[str, Any] | str:
        """Add a torrent from a magnet, HTTP URL, or local file."""
        url = "/torrents?&overwrite=true"
        if url_or_path.startswith("http"):
            url += "&is_url=true"
        if content:
            return await self._safe_request("POST", url, content=content)  # type: ignore
        if os.path.exists(url_or_path):
            try:
                with open(url_or_path, "rb") as f:
                    return await self._safe_request("POST", url, content=f.read())  # type: ignore
            except FileNotFoundError:
                return f"Error: File not found at {url_or_path}"
            except IOError as e:
                return f"Error reading file {url_or_path}: {e}"
        return await self._safe_request("POST", url, content=url_or_path)  # type: ignore

    async def create_torrent(self, folder_path: str) -> dict[str, Any] | str:
        """Create a torrent from a local folder and start seeding."""
        return await self._safe_request("POST", "/torrents/create", content=folder_path)  # type: ignore

    async def resolve_magnet(self, magnet_link: str) -> bytes | str:
        """Resolve a magnet link to torrent file bytes."""
        return await self._safe_request(
            "POST", "/torrents/resolve_magnet", content=magnet_link
        )  # type: ignore

    # Torrent specific
    async def get_torrent_details(self, id_or_infohash: str) -> dict[str, Any] | str:
        """Get details for a specific torrent."""
        return await self._safe_request("GET", f"/torrents/{id_or_infohash}")  # type: ignore

    async def get_torrent_stats(self, id_or_infohash: str) -> dict[str, Any] | str:
        """Get stats for a specific torrent."""
        return await self._safe_request("GET", f"/torrents/{id_or_infohash}/stats/v1")  # type: ignore

    async def get_torrent_haves(self, id_or_infohash: str) -> list[bool] | str:
        """Get the bitfield of have pieces for a torrent."""
        return await self._safe_request("GET", f"/torrents/{id_or_infohash}/haves")  # type: ignore

    async def get_torrent_metadata(self, id_or_infohash: str) -> bytes | str:
        """Download the .torrent file for a torrent."""
        return await self._safe_request("GET", f"/torrents/{id_or_infohash}/metadata")  # type: ignore

    async def get_torrent_playlist(self, id_or_infohash: str) -> str:
        """Get a playlist for a specific torrent."""
        content = await self._safe_request(
            "GET", f"/torrents/{id_or_infohash}/playlist"
        )
        if isinstance(content, str):
            return content
        return content  # type: ignore

    async def stream_torrent_file(
        self, id_or_infohash: str, file_idx: int, range_header: str | None = None
    ) -> AsyncGenerator[bytes, None] | str:
        """Stream a file from a torrent."""
        headers = {"Range": range_header} if range_header else {}
        path = f"/torrents/{id_or_infohash}/stream/{file_idx}"
        async for chunk in self._safe_stream_request("GET", path, headers=headers):  # type: ignore
            yield chunk

    async def pause_torrent(self, id_or_infohash: str) -> None | str:
        """Pause a torrent."""
        return await self._safe_request("POST", f"/torrents/{id_or_infohash}/pause")

    async def start_torrent(self, id_or_infohash: str) -> None | str:
        """Start (resume) a torrent."""
        return await self._safe_request("POST", f"/torrents/{id_or_infohash}/start")

    async def forget_torrent(self, id_or_infohash: str) -> None | str:
        """Forget a torrent, keeping the files."""
        return await self._safe_request("POST", f"/torrents/{id_or_infohash}/forget")

    async def delete_torrent(self, id_or_infohash: str) -> None | str:
        """Delete a torrent and its files."""
        return await self._safe_request("POST", f"/torrents/{id_or_infohash}/delete")

    async def add_peers(self, id_or_infohash: str, peers: list[str]) -> None | str:
        """Add peers to a torrent."""
        content = "\n".join(peers)
        return await self._safe_request(
            "POST", f"/torrents/{id_or_infohash}/add_peers", content=content
        )

    async def update_only_files(
        self, id_or_infohash: str, file_indices: list[int]
    ) -> None | str:
        """Change the selection of files to download."""
        return await self._safe_request(
            "POST",
            f"/torrents/{id_or_infohash}/update_only_files",
            json={"only_files": file_indices},
        )

    # Peer stats
    async def get_peer_stats(self, id_or_infohash: str) -> list[dict[str, Any]] | str:
        """Get per-peer stats for a torrent."""
        return await self._safe_request("GET", f"/torrents/{id_or_infohash}/peer_stats")  # type: ignore

    async def get_peer_stats_prometheus(self, id_or_infohash: str) -> str:
        """Get per-peer stats in Prometheus format."""
        content = await self._safe_request(
            "GET", f"/torrents/{id_or_infohash}/peer_stats/prometheus"
        )
        if isinstance(content, str):
            return content
        return content  # type: ignore
