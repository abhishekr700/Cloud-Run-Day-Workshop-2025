import datetime

from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_news(city: str) -> dict:
   """Retrieves the news of a particular city.
   Args:
       city (str): The name of the city for which to retrieve the news.

   Returns:
       dict: headline and content of the news, or error message.
   """
   if city.lower() == "bengaluru" or city.lower() == "bangalore":
       return {
           "headline": "Bengaluru police issue traffic advisory for August 10 amid PM Modi's visit",
           "content": "The Bengaluru Traffic Police have announced traffic restrictions on key routes on August 10 between 8:30 am and 2:30 pm amid Prime Minister Narendra Modi's scheduled visit to the city.",
       }
   else:
       return {
           "error_message": f"News for '{city}' is not available.",
       }

root_agent = Agent(
   name="news_assistant_agent",
   model="gemini-2.0-flash",
   description=(
       "Agent to retrieve news for any particular city."
   ),

   instruction=(
       "You are a helpful agent who can answer user questions related to news of any city."
   ),
   tools=[get_news],
)
