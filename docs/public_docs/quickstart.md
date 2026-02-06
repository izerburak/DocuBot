# Quickstart

## What this is
A lightweight demo web app that calls a local LLM and optionally enriches answers using Retrieval-Augmented Generation (RAG) over local documents.

## Requirements
- Python 3.10+
- Local LLM runtime installed and running (e.g., Ollama)
- Documents available in the configured docs directory

## Run (Typical)
1) Install dependencies
2) Start the Flask server
3) Open the web UI
4) Ask a question

## Notes
- For best results, ensure the document corpus includes relevant technical or policy content.
- If answers do not reference documents, run a reindex (if enabled) or verify the docs path.
