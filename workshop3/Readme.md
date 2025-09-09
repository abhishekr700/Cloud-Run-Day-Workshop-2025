# Readme

## Run Remote Agent

```bash
uvicorn remote_agents.sentiment_analyzer_agent.agent:a2a_app --host 0.0.0.0 --port 8001
```

## Run Orchestrator Agent

> Plug the url of remote agent in orchestrator first

```bash
uvicorn orchestrator.__main__:app --host 0.0.0.0 --port 8000
```


### Note
remote_agents/sentiment_analyzer_agent/agent_executor.py is obsolete file for now. It is not being used.
