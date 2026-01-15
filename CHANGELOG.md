## [0.10.0] - 2026-01-15

### ⚙️ Miscellaneous Tasks

- Chore: update changelog for v0.9.2 release
- Chore: replace mypy and pytest with ty, update config and bump version to 0.10.0

## [0.9.2] - 2025-11-28

### ⚙️ Miscellaneous Tasks

- Chore: bump version to 0.9.2

## [0.9.1] - 2025-09-30

### ⚙️ Miscellaneous Tasks

- Chore: bump version to 0.9.1
- Chore: bump version to 0.9.1 and update changelog

## [0.9.0] - 2025-08-25

### ⚙️ Miscellaneous Tasks

- Chore: update dependencies
- Chore: update changelog for v0.9.0 release with dependency updates

## [0.8.2] - 2025-08-16

### 📚 Documentation

- Docs: add docker installation instructions in README.md

### ⚙️ Miscellaneous Tasks

- Chore: update deps
- Chore: update changelog for v0.8.2 with docker docs and dependency updates

## [0.8.1] - 2025-08-06

### 🐛 Bug Fixes

- Fix: ci for docker hub

### 📚 Documentation

- Docs: add changelog entry for Docker Hub CI fixes in v0.8.1

## [0.8.0] - 2025-08-06

### ⚙️ Miscellaneous Tasks

- Chore: update cryptography from 45.0.5 to 45.0.6
- Chore: bump rqbit-mcp version from 0.7.1 to 0.8.0
- Ci: add Docker Hub publishing workflow and Dockerfile for container releases
- Chore: bump fastmcp dependency from 2.11.1 to 2.11.2
- Chore: update dependencies and add Docker Hub publishing workflow for v0.8.0
- Ci: enable Docker image push and upgrade pip in publish workflow

## [0.7.1] - 2025-08-04

### ⚙️ Miscellaneous Tasks

- Chore: update dependencies including anyio to 4.10.0 and cyclopts to 3.22.5
- Chore: update dependencies including anyio 4.10.0 and cyclopts 3.22.5

## [0.7.0] - 2025-07-20

### 🚀 Features

- Feat: add URL detection and overwrite flag to torrent addition endpoint

### 📚 Documentation

- Docs: add URL detection and overwrite flag feature to changelog

### ⚙️ Miscellaneous Tasks

- Chore: update ruff to 0.12.2 and optimize CI workflow with uv caching
- Chore: update dependencies including authlib 1.6.1 and fastmcp 2.10.6
- Chore: prepare release v0.7.0 with updated dependencies and changelog

## [0.6.1] - 2025-07-03

### 🚀 Features

- Feat: extend download_torrent to support HTTP URLs and local files in addition to magnet links
- Feat: extend download_torrent to support HTTP URLs and local files

## [0.6.0] - 2025-07-03

### 📚 Documentation

- Docs: add environment variables section to README.md
- Docs: clarify difference between forget_torrent and new delete_torrent commands

### ⚙️ Miscellaneous Tasks

- Chore: update dependencies, move/update docker setup, update readme
- Chore: update changelog for v0.6.0 with documentation and dependency updates

## [0.5.0] - 2025-06-30

### 🚀 Features

- Feat: add HTTP basic auth support and standardize JSON string responses

### 📚 Documentation

- Docs: add changelog entry for v0.5.0 with HTTP auth and JSON response features

## [0.4.0] - 2025-06-27

### 🚀 Features

- Feat: add restart policy for rqbit container to ensure continuous operation

### 🐛 Bug Fixes

- Fix: typos
- Fix: ports not needed in docker compose

### 🚜 Refactor

- Refactor: rename add_torrent to download_torrent and improve error handling
- Refactor: rename add_torrent to download_torrent for clarity and update examples

### ⚙️ Miscellaneous Tasks

- Chore: update mcp to v1.10.0 and add jsonschema dependencies
- Chore: upgrade fastmcp to 2.9.2 and downgrade mcp to 1.9.4
- Chore: update changelog for v0.4.0 with restart policy and API improvements

## [0.3.0] - 2025-06-24

### 🚀 Features

- Feat: add get_torrent_stats endpoint to fetch torrent statistics

### 🚜 Refactor

- Refactor: standardize os module imports and usage in client.py

### ⚙️ Miscellaneous Tasks

- Chore: bump rqbit-mcp version to 0.3.0
- Chore: prepare release v0.3.0 with torrent stats endpoint and client refactoring

## [0.2.0] - 2025-06-24

### 🚀 Features

- Feat: initialize rqbit MCP server with API wrapper and Docker setup

### 📚 Documentation

- Docs: add CHANGELOG.md to track project changes and releases

### 🧪 Testing

- Test: add MCP server tests and update badges in README
