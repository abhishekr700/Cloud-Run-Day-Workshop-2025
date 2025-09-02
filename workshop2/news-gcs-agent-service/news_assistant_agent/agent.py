# news_gcs_agent/news_assistant_agent/agent.py
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, SseConnectionParams, StdioServerParameters
from dotenv import load_dotenv

load_dotenv()

GCS_MCP_SERVER_URL = os.environ.get("GCS_MCP_SERVER_URL")
if not GCS_MCP_SERVER_URL:
    print("WARNING: GCS_MCP_SERVER_URL environment variable not set. The tool for GCS operations will not be available.")
    GCS_MCP_SERVER_URL="https://gcs-mcp-server-554461076311.us-central1.run.app"

# Toolset for Google News & Trends MCP Server (using uvx)
news_and_trends_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='uvx',
            args=['google-news-trends-mcp@latest'],
        ),
        timeout=30 # Increased timeout for potentially longer-running trend queries
    ),
    tool_filter=[
        'get_news_by_keyword',
        'get_news_by_location',
        'get_news_by_topic',
        'get_top_news',
        'get_trending_keywords',
    ]
)

# Toolset for the remote GCS MCP Server (using SSE)
gcs_tools = []
if GCS_MCP_SERVER_URL:
    gcs_toolset = MCPToolset(
        connection_params=SseConnectionParams(
            # MODIFIED: Connect to the correct /sse endpoint
            url=f"{GCS_MCP_SERVER_URL}/sse",
            headers={"Accept": "text/event-stream, application/json"},
            timeout=15
        ),
        tool_filter=['create_gcs_file', 'list_gcs_files']
    )
    gcs_tools.append(gcs_toolset)

all_tools = [news_and_trends_toolset] + gcs_tools

root_agent = LlmAgent(
    name="news_gcs_assistant",
    model="gemini-2.5-pro",
    description="Agent to fetch news and trends, and store summaries in GCS.",
    instruction="""You are a news and trends assistant. You have access to the following tools:

    **News & Trends Tools:**
    1.  `get_news_by_keyword`: Search for news using specific keywords.
    2.  `get_news_by_location`: Retrieve news relevant to a particular location.
    3.  `get_news_by_topic`: Get news based on a chosen topic.
    4.  `get_top_news`: Fetch the top news stories from Google News.
    5.  `get_trending_keywords`: Return trending keywords from Google Trends for a specified location.

    **Storage Tools:**
    6.  `create_gcs_file`: Saves text content to a file in Google Cloud Storage. Parameters: `bucket_name`, `destination_blob_name`, `content`.
    7.  `list_gcs_files`: Lists files in a GCS bucket.

    **VERY IMPORTANT:** You MUST use ONLY these provided tools. Do NOT write any Python code.

    **Workflow for saving news:**
    1.  Use one of the `get_news_*` tools or `get_top_news` with the correct parameters.
    2.  Summarize the results.
    3.  Call `create_gcs_file` to save the summary.
    """,
    tools=all_tools,
)


