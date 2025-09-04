import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm



OLLAMA_MODEL = "ollama/gemma:2b" # The model we pulled in the Ollama service
OLLAMA_SERVICE_URL = os.environ.get("OLLAMA_SERVICE_URL")
API_KEY = os.environ.get("GOOGLE_API_KEY")

# --- Agent Definition ---
root_agent = LlmAgent(
   model=LiteLlm(
       model=OLLAMA_MODEL,
       api_base=OLLAMA_SERVICE_URL,
       # Pass authentication headers if needed
       # extra_headers=auth_headers
       # Alternatively, if endpoint uses an API key:
       api_key=API_KEY
   ),
   name="ollama_agent",
   instruction="You are a helpful assistant running on a self-hosted vLLM endpoint.",
)
