import argparse

from .mcp_server import mcp


def cli() -> None:
    parser = argparse.ArgumentParser(description="Run Rqbit MCP Server.")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Mode to run the server in. Default: stdio.",
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind the server to."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to. Default: 8000.",
    )

    args = parser.parse_args()

    print(f"Starting MCP server on {args.host}:{args.port}")
    mcp.run(
        transport=args.mode,
        **({} if args.mode == "stdio" else {"host": args.host, "port": args.port}),
    )


if __name__ == "__main__":
    cli()
