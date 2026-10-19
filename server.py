import json
from pathlib import Path
from typing import Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel, Field

mcp = MCPServer("DevOps Learning Server")

DATA_FILE = Path(__file__).parent / "data" / "pipeline_runs.json"


# --- Data Models ---

class PipelineRun(BaseModel):
    run_id: int
    pipeline: str
    status: Literal["failed", "succeeded", "running"]
    duration_seconds: int | None = None
    
    
class PipelineRuns(BaseModel):
    runs: list[PipelineRun]
    
    
class PipelineLog(BaseModel):
    run_id: int
    pipeline: str
    log: str = Field(description="Execution log of the pipeline run")
    
    
# --- Data Access ---

def load_runs() -> list[dict]:
    """Read pipeline runs from the local JSON file."""
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)
    
    
# --- MCP Tools ---

@mcp.tool()
def list_pipeline_runs(
    status: Literal["all", "failed", "succeeded", "running"] = "all",
    pipeline_name: str | None = None
) -> PipelineRuns:
    """List CI/CD pipeline runs.
    
    Filter runs by execution status and/or exact pipeline name.
    Returns pipeline run IDs that can be used with get_pipeline_log.
    This tool only reads data and does not modify pipelines.
    """
    
    runs: list[dict] = list(load_runs())
    
    if status != "all":
        runs = [
            run for run in runs
            if run["status"] == status
        ]
        
    if pipeline_name is not None:
        runs = [
            run for run in runs
            if run["pipeline"] == pipeline_name
        ]
        
    return PipelineRuns(
        runs=[
            PipelineRun(
                run_id=run["run_id"],
                pipeline=run["pipeline"],
                status=run["status"],
                duration_seconds=run["duration_seconds"],
            )
            for run in runs
        ]
    )
    
    
@mcp.tool()
def get_pipeline_log(run_id: int) -> PipelineLog:
    """Get the execution log of a CI/CD pipeline run by its run ID."""
    
    runs: list[dict] = list(load_runs())
    
    for run in runs:
        if run["run_id"] == run_id:
            return PipelineLog(
                run_id=run["run_id"],
                pipeline=run["pipeline"],
                log=run["log"]
            )
        
    raise ToolError(f"Pipeline run {run_id} was not found.")
