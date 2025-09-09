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
           "headline": "Upto 6 hour long traffic Jams in Bengaluru on 9th September",
           "content": "Due to extremely heavy rainfall, parts of Bengaluru, including Whitefield and MG Road experienced long traffic jams due to waterlogging.",
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
