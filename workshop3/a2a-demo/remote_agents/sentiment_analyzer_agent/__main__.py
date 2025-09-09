"""
Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from a2a.types import AgentCapabilities, AgentSkill, AgentCard
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import InMemoryTaskStore
from agent import root_agent
from agent_executor import ADKAgentExecutor
import uvicorn
from dotenv import load_dotenv
import logging
import os
import click
from google.adk.runners import Runner
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--host", "host", default="0.0.0.0")
@click.option("--port", "port", default=8080)
def main(host, port):
    """Entry point for the A2A Sentiment Analyzer Agent."""
    try:
        run_port = int(os.environ.get("PORT", port))
        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id="analyze_sentiment",
            name="Sentiment Analysis Tool",
            description="Helps with analyzing sentiment from a news article",
            tags=["sentiment analysis"],
            examples=[
                "Analyze the sentiment of this article: <article text>"
            ],
        )
        agent_host_url = (
            os.getenv("HOST_OVERRIDE")
            if os.getenv("HOST_OVERRIDE")
            else f"http://{host}:{run_port}/"
        )
        agent_card = AgentCard(
            name="sentiment_analyzer_agent",
            description="Helps with analyzing sentiment from a news article",
            url=agent_host_url,
            version="1.0.0",
            defaultInputModes=["text"],
            defaultOutputModes=["text"],
            capabilities=capabilities,
            skills=[skill],
        )

        runner = Runner(
            agent=root_agent,
            memory_service=InMemoryMemoryService(),
            session_service=InMemorySessionService(),
            app_name="sentiment_analyzer_agent",
        )

        request_handler = DefaultRequestHandler(
            agent_executor=ADKAgentExecutor(runner=runner, agent_card=agent_card),
            task_store=InMemoryTaskStore(),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        uvicorn.run(server.build(), host=host, port=run_port)

        logger.info(f"Starting server on {host}:{run_port}")
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main()
