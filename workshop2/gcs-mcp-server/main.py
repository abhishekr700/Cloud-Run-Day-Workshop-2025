# gcs_mcp_server/main.py
import asyncio
import logging
import os
import json

from fastmcp import FastMCP
from google.cloud import storage
from mcp import types as mcp_types

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("GCS MCP Server")

try:
    storage_client = storage.Client()
    logger.info("Google Cloud Storage client initialized successfully..")
except Exception as e:
    logger.error(f"Failed to initialize Google Cloud Storage client: {e}")
    storage_client = None

def check_client():
    if storage_client is None:
        raise Exception("Google Cloud Storage client is not initialized.")
    return True

@mcp.tool()
async def create_gcs_file(bucket_name: str, destination_blob_name: str, content: str) -> mcp_types.TextContent:
    """Creates a new file (blob) in a GCS bucket with the given content.

    Args:
        bucket_name: Name of the bucket in which the file needs to be created.
        destination_blob_name: Name of the file that will be created.
        content: Contents of the file.
    """
    check_client()
    logger.info(f"Attempting to create file '{destination_blob_name}' in bucket '{bucket_name}'.")
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(content)
        msg = f"File '{destination_blob_name}' created successfully in bucket '{bucket_name}'."
        logger.info(msg)
        return mcp_types.TextContent(type="text", text=json.dumps({"status": "success", "message": msg}))
    except Exception as e:
        logger.error(f"Error creating file: {e}")
        return mcp_types.TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))

@mcp.tool()
async def list_gcs_files(bucket_name: str, prefix: str = None) -> mcp_types.TextContent:
    """Lists all files (blobs) in a GCS bucket, optionally filtered by a prefix.

    Args:
        bucket_name (str): The name of the GCS bucket.
        prefix (str, optional): A prefix to filter the listed files.
    """
    check_client()
    logger.info(f"Listing files in bucket '{bucket_name}' with prefix '{prefix}'.")
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        files = [blob.name for blob in blobs]
        logger.info(f"Files found: {files}")
        return mcp_types.TextContent(type="text", text=json.dumps({"status": "success", "files": files}))
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return mcp_types.TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"GCS MCP server starting on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="sse",
            host="0.0.0.0",
            port=port,
        )
    )

