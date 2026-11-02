# Building an AI-Ready DevOps MCP Server

## Overview

A four-week mini-learning project exploring the Model Context Protocol (MCP) and its integration into AI-driven DevOps workflows.

**Goal:** Understand MCP architecture, implement a custom MCP server, examine protocol communication, and demonstrate AI-driven tool execution.

## ArchitectureW

The solution consists of:

- **AI Host:** VS Code with GitHub Copilot
- **MCP Client:** Integrated into the AI Host
- **MCP Server:** Custom Python implementation using the MCP SDK
- **Data Source:** Simulated CI/CD pipeline execution data in JSON format

The MCP server exposes two read-only tools:

| Tool | Description |
|---|---|
| `list_pipeline_runs` | Retrieve pipeline executions, optionally filtered by status and pipeline name |
| `get_pipeline_log` | Retrieve execution logs for a specific pipeline run |

## Getting Started

Requirements: Python, uv, and an MCP-compatible client.

Install dependencies:

```bash
uv sync
```

Start the MCP Inspector for local testing:

```bash
uv run mcp dev server.py
```

Connect the server to an MCP-compatible AI Host to enable AI-driven tool execution.

## Learning Journey

### Week 1 – MCP Fundamentals

- Explored MCP Host, Client, and Server architecture
- Implemented a first MCP server
- Tested tool discovery and execution
- Compared MCP with traditional REST APIs

### Week 2 – Custom DevOps Tools

- Implemented tools for retrieving pipeline runs and logs
- Added filtering, Pydantic data models, and structured output
- Explored input validation and error handling

### Week 3 – Protocol & Communication

- Explored JSON-RPC messages and MCP transports
- Implemented a custom client communicating over stdio
- Examined tool schemas and structured responses
- Implemented basic tool orchestration

### Week 4 – AI Integration

- Connected the MCP server to GitHub Copilot in VS Code
- Demonstrated AI-driven tool selection and execution
- Evaluated tool chaining and pipeline-failure analysis

## Final Experiment

**User request:**

"Investigate failed backend-deploy pipeline runs. Retrieve their logs, identify the observed errors, and explain possible causes."

**Observed agent behavior:**

1. Called `list_pipeline_runs` to discover failed deployments.
2. Identified pipeline run 101.
3. Called `get_pipeline_log` with the discovered run ID.
4. Identified `ImagePullBackOff` in the execution log.
5. Distinguished observed facts from possible root causes.

**Result:** Successful native MCP tool integration and AI-driven tool orchestration.

## Key Learnings

- MCP standardizes how AI applications discover and invoke external tools.
- MCP does not replace REST APIs or provide LLM reasoning itself.
- Tool descriptions and schemas are important for reliable tool selection.
- Structured outputs enable predictable processing of tool results.
- The AI model can select tools dynamically, while the host controls their execution.
- Tool execution and AI-generated diagnoses must be validated separately.

## Limitations & Future Improvements

- The current implementation uses simulated rather than real CI/CD data.
- The solution has only been evaluated against a small number of test scenarios.
- Authentication, authorization, and prompt-injection defenses have not been comprehensively tested.
- The next step would be integration with Azure DevOps or GitHub Actions APIs, followed by automated tests and stronger security controls.

## Conclusion

The project successfully demonstrated how a custom MCP server can expose DevOps functionality to an AI application through a standardized interface.

The main takeaway is that MCP separates tool integration from AI-driven decision-making, allowing existing DevOps capabilities to become reusable building blocks for agentic workflows.
