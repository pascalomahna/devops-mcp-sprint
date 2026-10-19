from mcp.server import MCPServer

# Create an MCP server
mcp = MCPServer("DevOps Learning Server")


@mcp.tool()
def get_pipeline_status(pipeline_name: str) -> str:
    """Get the latest execution status of a CI/CD pipeline."""
    
    pipelines = {
        "backend-deploy": "failed",
        "frontend-test": "succeeded",
    }
    
    status = pipelines.get(pipeline_name)
    
    if status is None:
        return f"Pipeline '{pipeline_name}' not found."
    
    return f"Pipeline '{pipeline_name}' status: {status}"
