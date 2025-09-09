import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
import uvicorn


logger = logging.getLogger(__name__)

load_dotenv()

AGENT_DIR = os.path.dirname(__file__)
SERVE_WEB_INTERFACE = True

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=SERVE_WEB_INTERFACE,
)

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
