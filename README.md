# Multi-Agent AI Orchestrator

This Jupyter Notebook demonstrates a **multi-agent AI system** using LangChain, LangGraph, and specialized tools.  
It creates a **Supervisor Agent** that coordinates three specialized sub-agents:

- **Coder Agent** – Writes, reviews, and executes code.
- **Files Agent** – Reads, writes, updates, and deletes files.
- **Research Agent** – Searches the internet for relevant information.

## Features
- Uses **LangChain** for prompt management and agent creation.
- Integrates **OpenRouter** models and **Tavily Search**.
- Supports autonomous multi-step task execution.
- Handles both code execution and file operations.
- Modular design using `StateGraph` for workflow management.

## Requirements
- Python 3.10+
- Jupyter Notebook
- Required libraries (install via pip):
  ```bash
  pip install langchain langgraph langchain-openai langchain-tavily langchain-community pydantic