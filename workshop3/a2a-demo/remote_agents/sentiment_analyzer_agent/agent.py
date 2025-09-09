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

import os
import urllib.error
import urllib.request

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types


def get_news_article(article_url: str) -> str:
  """Get a news article from a URL."""
  try:
    with urllib.request.urlopen(article_url) as response:
      return response.read().decode('utf-8')
  except urllib.error.URLError as e:
    return f'Error fetching article: {e}'


root_agent = Agent(
    model='gemini-2.0-flash',
    name='sentiment_analyzer_agent',
    description='An agent that analyzes the sentiment of news articles.',
    instruction="""
      You are a sentiment analyzer. 
      You will be provided with a link to a news article. If the link is valid, fetch the contents of the article using get_news_article tool.
      When given a news article is valid, check and respond with the sentiment of the article.
      If multiple articles are provided, respond with the sentiment of each article.
    """,
    tools=[
        get_news_article,
    ],
    # planner=BuiltInPlanner(
    #     thinking_config=types.ThinkingConfig(
    #         include_thoughts=True,
    #     ),
    # ),
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)

