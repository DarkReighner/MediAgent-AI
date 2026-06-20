 # MediAgent

AI-powered Medical Prior Authorization Assistant built using LangGraph, Qwen3, ChromaDB, FastAPI, and Python.

## Features

- PDF Clinical Note Upload
- AI Medical Fact Extraction (Qwen3 via Ollama)
- Retrieval-Augmented Generation (ChromaDB)
- Multi-Agent Workflow (LangGraph)
- Explainable Authorization Decisions
- Audit Logging
- Interactive Dashboard

## Workflow

Clinical Note
↓
Extraction Agent
↓
Retrieval Agent
↓
Decision Agent
↓
Audit Agent
↓
Final Recommendation

## Tech Stack

- Python
- FastAPI
- LangGraph
- Qwen3 (Ollama)
- ChromaDB
- HTML/CSS

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/ui
```


## Future Improvements

- FHIR R4 APIs
- Advanced Policy Corpus
- React Dashboard
- Healthcare Analytics
