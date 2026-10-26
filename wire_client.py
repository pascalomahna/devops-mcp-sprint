import json
import subprocess


# Metadata required for modern MCP protocol
META = {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientInfo": {
        "name": "DevOpsLearningClient",
        "version": "1.0.0"
    },
    "io.modelcontextprotocol/clientCapabilities": {}
}


def send_request(process, request_id, method, params=None):
    """Send a JSON-EPC request over stdio."""
    
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": {
            **(params or {}),
            "_meta": META
        }
    }
    
    # JSON-RPC messages are newline-delimited
    message = json.dumps(request)
    
    print("\n>>> REQUEST")
    print(json.dumps(request, indent=2))
    
    process.stdin.write(message + "\n")
    process.stdin.flush()
    
    # Read the corresponding server response
    response_line = process.stdout.readline()
    
    if not response_line:
        raise RuntimeError("Server closed the connection")
    
    response = json.loads(response_line)
    
    print("\n<<< RESPONSE")
    print(json.dumps(response, indent=2))
    
    return response


# Start our MCP server as a child process
process = subprocess.Popen(
    ["uv", "run", "mcp", "run", "server.py",
     "--transport", "stdio"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    encoding="utf-8"
)

try:
    # 1. Discover server capabilities
    send_request(process, 1, "server/discover")
    
    # 2. Discover available tools
    tools = send_request(process, 2, "tools/list")
    
    # 3. Execute a tool
    result = send_request(
        process,
        3,
        "tools/call",
        {
            "name": "list_pipeline_runs",
            "arguments": {
                "status": "failed",
                "pipeline_name": "backend-deploy"
            }
        }
    )

    # Check for a protocol error
    if "error" in result:
        print("MCP protocol error:", result["error"])

    else:
        tool_result = result["result"]

        # Check for a tool execution error
        if tool_result.get("isError", False):
            print("Tool execution failed:", tool_result["content"])

        else:
            runs = tool_result.get("structuredContent", {}).get("runs", [])

            if not runs:
                print("No matching pipeline runs found.")

            else:
                run_id = runs[0]["run_id"]

                log_result = send_request(
                    process,
                    4,
                    "tools/call",
                    {
                        "name": "get_pipeline_log",
                        "arguments": {
                            "run_id": run_id
                        }
                    }
                )

                if "error" in log_result:
                    print("MCP protocol error:", log_result["error"])
                elif log_result["result"].get("isError", False):
                    print("Tool execution failed:", log_result["result"]["content"])
                else:
                    log = log_result["result"].get("structuredContent", {}).get("log")
                    print("Pipeline log:", log)
    
finally:
    # Stop the server process cleanly
    process.stdin.close()
    
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
