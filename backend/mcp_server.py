import asyncio
import json
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from openmetadata import OpenMetadataClient
from dotenv import load_dotenv

load_dotenv()

server = Server("metabot-openmetadata")

# Auto-login to sandbox — no bot token required
om = OpenMetadataClient(
    base_url=os.getenv("OM_BASE_URL", "https://sandbox.open-metadata.org"),
    token=os.getenv("OM_TOKEN", ""),
)


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_tables",
            description="Search for tables in OpenMetadata Sandbox by keyword or name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword or table name"}
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_table_details",
            description="Get full details of a table: columns, owner, tags, description.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_fqn": {"type": "string", "description": "Fully qualified table name"}
                },
                "required": ["table_fqn"],
            },
        ),
        types.Tool(
            name="get_table_owner",
            description="Get the owner of a specific table.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_fqn": {"type": "string", "description": "Fully qualified table name"}
                },
                "required": ["table_fqn"],
            },
        ),
        types.Tool(
            name="get_lineage",
            description="Get upstream and downstream lineage of a table.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_fqn": {"type": "string", "description": "Fully qualified table name"}
                },
                "required": ["table_fqn"],
            },
        ),
        types.Tool(
            name="list_recently_updated",
            description="List the most recently updated tables in OpenMetadata Sandbox.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "search_tables":
            result = om.search_tables(arguments.get("query", ""))
        elif name == "get_table_details":
            result = om.get_table_details(arguments.get("table_fqn", ""))
        elif name == "get_table_owner":
            result = om.get_table_owner(arguments.get("table_fqn", ""))
        elif name == "get_lineage":
            result = om.get_lineage(arguments.get("table_fqn", ""))
        elif name == "list_recently_updated":
            result = om.list_recently_updated()
        else:
            result = {"error": f"Unknown tool: {name}"}
    except Exception as e:
        result = {"error": str(e)}

    return [types.TextContent(type="text", text=json.dumps(result, default=str))]


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
