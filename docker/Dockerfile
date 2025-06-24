FROM ghcr.io/astral-sh/uv:python3.13-alpine
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-editable
COPY rqbit_client/ ./rqbit_client/

EXPOSE 8000

CMD ["uv", "run", "--locked", "--no-sync", "-m", "rqbit_client", "--mode", "sse"]