import asyncio
import json

from mcp import Client
from server import mcp


async def main():
    # Connect directly to our MCP server
    async with Client(mcp) as client:
        
        # 1. Inspect protocol information
        print("Protocol:", client.protocol_version)
        
        # 2. Discover available tools
        response = await client.list_tools()
        
        for tool in response.tools:
            print("\nTool:", tool.name)
            print("Description:", tool.description)
            print("Input schema:")
            print(json.dumps(tool.input_schema, indent=2))
            
        result = await client.call_tool(
            "list_pipeline_runs",
            {"status": "failed"}
        )

        print("Is error:", result.is_error)
        print("Structured content:", result.structured_content)
        print("Run-ID: ", result.structured_content["runs"][0]["run_id"])
            
        # 3. Execute our DevOps tool
        #result = await client.call_tool(
        #    "get_pipeline_status",
        #    {"wrong_parameter": "backend-deploy"}
        #)
        
        #print("\nTool result:")
        #print("Is error:", result.is_error)
        
        #for block in result.content:
        #    if block.type == "text":
        #        print(block.text)
                
                
asyncio.run(main())
