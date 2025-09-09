# Readme

## Run Remote Agent
Local run
```bash
uvicorn remote_agents.sentiment_analyzer_agent.agent:a2a_app --host 0.0.0.0 --port 8001
```

## Run Orchestrator Agent
Run locally
> Plug the url of remote agent in orchestrator first

```bash
uvicorn orchestrator.__main__:app --host 0.0.0.0 --port 8000
```

