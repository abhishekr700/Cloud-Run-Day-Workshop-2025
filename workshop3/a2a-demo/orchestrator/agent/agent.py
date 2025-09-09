# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import urllib.error
import urllib.request

from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.example_tool import ExampleTool
from google.genai import types


# --- Sentiment Analyzer Agent ---
REMOTE_SENTIMENT_AGENT_URL = "https://sentiment-analyzer-agent-xxxxxxxx.us-central1.run.app"
# REMOTE_AGENT_URL = "http://localhost:8001"

# --- Business Analyzer Agent ---
REMOTE_BUSINESS_AGENT_URL = "https://business-analyzer-agent-xxxxxxxx.us-central1.run.app"


# --- Summarizer Sub-Agent ---
def summarize_article(article: str) -> str:
  """Summarizes a news article."""
  return f"This is a summary of the article: {article[:100]}..."

def get_news_article(article_url: str) -> str:
  """Get a news article from a URL."""
  try:
    with urllib.request.urlopen(article_url) as response:
      return response.read().decode('utf-8')
  except urllib.error.URLError as e:
    return f'Error fetching article: {e}'




summarizer_agent = Agent(
    name="summarizer_agent",
    description="Handles summarizing news articles.",
    instruction="""
      You are responsible for summarizing news articles based on the user's request.
      When asked to summarize an article, you must call the summarize_article tool with the article content.
    """,
    tools=[summarize_article],
)


example_tool = ExampleTool([
    {
        "input": {
            "role": "user",
            "parts": [
                {"text": "Summarize this article: 'A new study shows...'"}
            ],
        },
        "output": [{
            "role": "model",
            "parts": [{"text": "Summary: A new study shows..."}],
        }],
    },
    {
        "input": {
            "role": "user",
            "parts": [{
                "text": (
                    "What is the sentiment of this article: 'The economy is"
                    " booming.'?"
                )
            }],
        },
        "output": [{
            "role": "model",
            "parts": [{"text": "The sentiment is positive."}],
        }],
    },
    {
        "input": {
            "role": "user",
            "parts": [{
                "text": (
                    "Summarize this article and then tell me its sentiment:"
                    " 'The new movie is a hit.'"
                )
            }],
        },
        "output": [
            {
                "role": "model",
                "parts": [{"text": "Summary: The new movie is a hit."}],
            },
            {
                "role": "model",
                "parts": [{"text": "The sentiment is positive."}],
            },
        ],
    },
])

sentiment_analyzer_agent = RemoteA2aAgent(
    name="sentiment_analyzer_agent",
    description="Agent that handles analyzing the sentiment of news articles.",
    agent_card=(
        # AGENT_CARD_WELL_KNOWN_PATH = "/.well-known/agent.json"
        f"{REMOTE_SENTIMENT_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

business_analyzer_agent = RemoteA2aAgent(
    name="business_analyzer_agent",
    description="Agent that handles analyzing the business impact of news articles.",
    agent_card=(
        # AGENT_CARD_WELL_KNOWN_PATH = "/.well-known/agent.json"
        f"{REMOTE_BUSINESS_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)


root_agent = Agent(
    model="gemini-2.0-flash",
    name="root_agent",
    instruction="""
      You are a helpful assistant that can fetch and analyze news articles with the help of other agents.
      Do not perform any kind of analysis on the articles yourself. Always ask other agents to provide for analysis.
      0. Fetch the article content using the get_news_article tool and then follow next steps.
      1. If the user asks to summarize an article, delegate to the summarizer_agent.
      2. If the user asks for sentiment analysis, delegate to the sentiment_analyzer_agent with article content as input.
      3. If the user asks for business impact analysis, delegate to the business_analyzer_agent with article content as input.
      4. If the user asks to summarize an article and then analyze its sentiment, call summarizer_agent with article content as input, then pass the result to sentiment_analyzer_agent.
      5. If the user asks to summarize an article and then analyze its business impact, call summarizer_agent with article content as input, then pass the result to business_analyzer_agent.
      Always clarify the results before proceeding.
    """,
    global_instruction="You are NewsBot, ready to analyze news articles.",
    sub_agents=[summarizer_agent, sentiment_analyzer_agent, business_analyzer_agent],
    tools=[get_news_article, example_tool],
)


