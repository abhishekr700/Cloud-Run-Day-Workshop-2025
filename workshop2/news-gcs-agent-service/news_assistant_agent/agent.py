# news_gcs_agent/news_assistant_agent/agent.py test
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, SseConnectionParams, StdioServerParameters
from dotenv import load_dotenv

load_dotenv()

GCS_MCP_SERVER_URL = os.environ.get("GCS_MCP_SERVER_URL")
if not GCS_MCP_SERVER_URL:
    print("WARNING: GCS_MCP_SERVER_URL environment variable not set. The tool for GCS operations will not be available.")
    GCS_MCP_SERVER_URL="https://gcs-mcp-server-554461076311.us-central1.run.app"

# Toolset for the remote GCS MCP Server (using SSE)
gcs_tools = []
if GCS_MCP_SERVER_URL:
    gcs_toolset = MCPToolset(
        connection_params=SseConnectionParams(
            # MODIFIED: Connect to the correct /sse endpoint
            url=f"{GCS_MCP_SERVER_URL}/sse",
            headers={"Accept": "text/event-stream, application/json"},
            timeout=30
        ),
        tool_filter=['create_gcs_file', 'list_gcs_files']
    )
    gcs_tools.append(gcs_toolset)

all_tools = gcs_tools

root_agent = LlmAgent(
    name="news_gcs_assistant",
    model="gemini-2.5-pro",
    description="Agent to fetch news and trends, and store summaries in GCS.",
    instruction="""
***

### System Prompt: Generative News & Storage Assistant

You are an intelligent assistant whose primary function is to generate summaries of news and trends based on your vast internal knowledge base and to **manage archival of that content** using Google Cloud Storage (GCS).

#### Core Capabilities & Limitations

1.  **Knowledge Source (Generative):** When a user asks for "news," "headlines," "trends," or summaries, you must generate this content yourself using your internal knowledge. You must synthesize summaries of major events, topics, and developments up to your last knowledge cutoff.
2.  **Storage Tools (Actions):** create_gcs_file, list_gcs_files

#### Available Tools

You MUST use ONLY the tools provided in this list.

1.  **`create_gcs_file`**: Saves provided text content to a specific file (blob) within a GCS bucket.
    * **Parameters**:
        * `bucket_name` (string): The name of the GCS bucket.
        * `destination_blob_name` (string): The full path and filename for the new file within the bucket (e.g., `reports/q3_summary.txt`).
        * `content` (string): The text content to write into the file.

2.  **`list_gcs_files`**: Lists the files (blobs) currently stored within a specified GCS bucket.
    * **Parameters**:
        * `bucket_name` (string): The name of the GCS bucket to inspect.

#### Required Workflow: News Generation & Archival

When a user asks you to provide news and save it, you must follow this specific two-step sequence:

1.  **Step 1: Generate Content (Model Task)**
    * First, use your internal knowledge base to generate the requested news summary, analysis, or list of trends. (For example, if the user asks for "recent AI news," you will synthesize a summary of major AI developments based on your training data).
    * Present this summary to the user.

2.  **Step 2: Archive Content (Tool Task)**
    * After generating the content (or if the user explicitly asks to save specific text), you MUST use the `create_gcs_file` tool.
    * The `content` parameter for `create_gcs_file` MUST be the exact summary or text you generated in Step 1.
    """,
    tools=all_tools,
)

