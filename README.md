# Python API Wrapper & MCP Server for rqbit

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://docs.astral.sh/uv/getting-started/installation/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![PyPI](https://badge.fury.io/py/rqbit-mcp.svg?cache-control=no-cache)](https://badge.fury.io/py/rqbit-mcp)
[![Actions status](https://github.com/philogicae/rqbit-mcp/actions/workflows/python-package-ci.yml/badge.svg?cache-control=no-cache)](https://github.com/philogicae/rqbit-mcp/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/philogicae/rqbit-mcp)

This repository provides a Python API wrapper and an MCP (Model Context Protocol) server for the [rqbit](https://github.com/ikatson/rqbit) torrent client. It allows for easy integration into other applications or services.

<a href="https://glama.ai/mcp/servers/@philogicae/rqbit-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@philogicae/rqbit-mcp/badge?cache-control=no-cache" alt="Rqbit MCP server" />
</a>

## Table of Contents

- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
  - [Installation](#installation)
    - [Install from PyPI (Recommended)](#install-from-pypi-recommended)
    - [For Local Development](#for-local-development)
    - [For Docker](#for-docker)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [As Python API Wrapper](#as-python-api-wrapper)
  - [As MCP Server](#as-mcp-server)
  - [Via MCP Clients](#via-mcp-clients)
    - [Example with Windsurf](#example-with-windsurf)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

## Features

-   API wrapper for the `rqbit` torrent client.
-   MCP server interface for standardized communication (stdio, sse, streamable-http)
-   Tools:
    -   `list_torrents`: List all torrents and their details.
    -   `download_torrent`: Download a torrent from a magnet link or a file.
    -   `get_torrent_details`: Get detailed information about a specific torrent.
    -   `get_torrent_stats`: Get stats/status of a specific torrent.
    -   `pause_torrent`: Pause a torrent.
    -   `start_torrent`: Start a torrent.
    -   `forget_torrent`: Forget a torrent, keeping the files.
    -   `delete_torrent`: Delete a torrent and its files.

## Setup

### Prerequisites

-   An running instance of [rqbit](https://github.com/ikatson/rqbit). (Included in docker compose)
-   Python 3.10+ (required for PyPI install).
-   [`uv`](https://github.com/astral-sh/uv) (for local development)

### Configuration

This application requires the URL of your `rqbit` instance.

**Set Environment Variable**: Copy `.env.example` to `.env` in your project's root directory and edit it with your settings. The application will automatically load variables from `.env`:
- MCP Server:
  - `RQBIT_URL`: The URL of the rqbit instance (Default: `http://localhost:3030`).
  - `RQBIT_HTTP_BASIC_AUTH_USERPASS`: If setup in rqbit instance.
- Rqbit Instance:
  - `RQBIT_HTTP_BASIC_AUTH_USERPASS`: The username and password for basic authentication, in the format `username:password`.
  - `RQBIT_HTTP_API_LISTEN_ADDR`: The listen address for the HTTP API (e.g., `0.0.0.0:3030`).
  - `RQBIT_UPNP_SERVER_ENABLE`: Enables or disables the UPnP server (e.g., `true` or `false`).
  - `RQBIT_UPNP_SERVER_FRIENDLY_NAME`: The friendly name for the UPnP server (e.g., `rqbit-media`).
  - `RQBIT_EXPERIMENTAL_UTP_LISTEN_ENABLE`: Enables or disables the uTP listener (Default: `false`).
  - Check [rqbit](https://github.com/ikatson/rqbit) for other variables and more information.


### Installation

Choose one of the following installation methods.

#### Install from PyPI (Recommended)

This method is best for using the package as a library or running the server without modifying the code.

1.  Install the package from PyPI:
```bash
pip install rqbit-mcp
```
2.  Create a `.env` file in the directory where you'll run the application and add your `rqbit` URL:
```env
RQBIT_URL=http://localhost:3030
```
3.  Run the MCP server (default: stdio):
```bash
python -m rqbit_client
```

#### For Local Development

This method is for contributors who want to modify the source code.
Using [`uv`](https://github.com/astral-sh/uv):

1.  Clone the repository:
```bash
git clone https://github.com/philogicae/rqbit-mcp.git
cd rqbit-mcp
```
2.  Install dependencies using `uv`:
```bash
uv sync --locked
```
3.  Create your configuration file by copying the example and add your settings:
```bash
cp .env.example .env
```
4.  Run the MCP server (default: stdio):
```bash
uv run -m rqbit_client
```

#### For Docker

This method uses Docker to run the server in a container.
compose.yaml includes [rqbit](https://github.com/ikatson/rqbit) torrent client.

1.  Clone the repository (if you haven't already):
```bash
git clone https://github.com/philogicae/rqbit-mcp.git
cd rqbit-mcp
```
2.  Create your configuration file by copying the example and add your settings:
```bash
cp .env.example .env
```
3.  Build and run the container using Docker Compose (default port: 8000):
```bash
docker compose up --build -d
```
4.  Access container logs:
```bash
docker logs rqbit-mcp -f
```

## Usage

### As Python API Wrapper

```python
import asyncio
from rqbit_client.wrapper import RqbitClient

async def main():
    # Read the RQBIT_URL from the .env file or fallback to default (http://localhost:3030)
    async with RqbitClient() as client:
        # Download a torrent
        magnet_link = "magnet:?xt=urn:btih:..."
        torrent = await client.download_torrent(magnet_link)
        print(torrent)

        # Check status
        status = await client.get_torrent_stats(torrent["id"])
        print(status)

        # List torrents
        torrents = await client.list_torrents()
        print(torrents)

if __name__ == "__main__":
    asyncio.run(main())
```

### As MCP Server

```python
from rqbit_client import RqbitMCP

RqbitMCP.run(transport="sse") # 'stdio', 'sse', or 'streamable-http'
```

### Via MCP Clients

Usable with any MCP-compatible client. Available tools:

-   `list_torrents`: List all torrents.
-   `download_torrent`: Download a torrent via magnet link or file path.
-   `get_torrent_details`: Get details of a specific torrent.
-   `get_torrent_stats`: Get stats/status of a specific torrent.
-   `pause_torrent`: Pause a torrent.
-   `start_torrent`: Start a torrent.
-   `forget_torrent`: Forget a torrent, keeping the files.
-   `delete_torrent`: Delete a torrent and its files.

#### Example with Windsurf

Configuration:
```json
{
  "mcpServers": {
    ...
    # with stdio (only requires uv)
    "rqbit-mcp": {
      "command": "uvx",
      "args": [ "rqbit-mcp" ],
      "env": { 
        "RQBIT_URL": "http://localhost:3030", # (Optional) Default rqbit instance URL
        "RQBIT_HTTP_BASIC_AUTH_USERPASS": "username:password" # (Optional) Only if setup in rqbit instance
      }
    },
    # with sse transport (requires installation)
    "rqbit-mcp": {
      "serverUrl": "http://127.0.0.1:8000/sse"
    },
    # with streamable-http transport (requires installation)
    "rqbit-mcp": {
      "serverUrl": "http://127.0.0.1:8000/mcp" 
    },
    ...
  }
}
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes to this project.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.