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

from pydantic import BaseModel
import uuid
from crewai import Agent, Crew, LLM, Task, Process
from crewai.tools import tool
from dotenv import load_dotenv
import litellm
import os

load_dotenv()

litellm.vertex_project = os.getenv("GOOGLE_CLOUD_PROJECT")
litellm.vertex_location = os.getenv("GOOGLE_CLOUD_LOCATION")


class ImpactedBusinessArea(BaseModel):
    area_name: str
    impact_level: str
    summary: str


class BusinessImpactReport(BaseModel):
    report_id: str
    status: str
    impacted_areas: list[ImpactedBusinessArea]


@tool("analyze_impact")
def analyze_business_impact(impacted_areas: list[ImpactedBusinessArea]) -> str:
    """
    Creates a new business impact report with the given impacted areas.

    Args:
        impacted_areas: List of impacted business areas to be added to the report.

    Returns:
        str: A message indicating that the report has been created.
    """
    try:
        report_id = str(uuid.uuid4())
        report = BusinessImpactReport(
            report_id=report_id, status="created", impacted_areas=impacted_areas
        )
        print("===")
        print(f"report created: {report}")
        print("===")
    except Exception as e:
        print(f"Error creating report: {e}")
        return f"Error creating report: {e}"
    return f"Report {report.model_dump()} has been created"


class BusinessAnalyzerAgent:
    TaskInstruction = """
# INSTRUCTIONS

You are a specialized business analyst assistant.
Your sole purpose is to analyze news articles and provide a business impact analysis.
If the user asks about anything other than business impact analysis of a news article, politely state that you cannot help with that topic.
Do not attempt to answer unrelated questions or use tools for other purposes.

# CONTEXT

Received user query with a news article: {user_prompt}
Session ID: {session_id}

# RULES

- When a user provides a news article, you will do the following:
    1. Analyze the article to identify key business areas that are impacted.
    2. For each area, determine the level of impact (e.g., High, Medium, Low) and provide a brief summary.
    3. Use the `analyze_business_impact` tool to structure this analysis.
    4. Finally, provide a response to the user with the detailed impact analysis and a report ID.
    
- Set response status to error if there is an error while processing the request.
- Set response status to completed if the request is complete.
"""
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def invoke(self, query, sessionId) -> str:
        model = LLM(
            model="vertex_ai/gemini-2.5-flash-lite",  # Use base model name without provider prefix
        )
        business_analyzer_agent = Agent(
            role="Business Analyzer Agent",
            goal=(
                "Analyze news articles and provide a business impact analysis for the user."
            ),
            backstory=("You are an expert and helpful business analyst agent."),
            verbose=False,
            allow_delegation=False,
            tools=[analyze_business_impact],
            llm=model,
        )

        analysis_task = Task(
            description=self.TaskInstruction,
            agent=business_analyzer_agent,
            expected_output="A structured business impact analysis report.",
        )

        crew = Crew(
            tasks=[analysis_task],
            agents=[business_analyzer_agent],
            verbose=False,
            process=Process.sequential,
        )

        inputs = {"user_prompt": query, "session_id": sessionId}
        response = crew.kickoff(inputs)
        return response


if __name__ == "__main__":
    agent = BusinessAnalyzerAgent()
    result = agent.invoke(
        "A new AI breakthrough promises to double chip performance, potentially disrupting the entire semiconductor industry.",
        "default_session",
    )
    print(result)
