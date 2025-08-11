# Multi-Agent AI Orchestrator

**Multi-Agent AI Orchestrator** is a modular multi-agent system where a **Supervisor** coordinates specialized agents to perform complex, multi-step AI-driven tasks.  
The agents work together to process input, conduct research, write code, manipulate files, and deliver a final answer to the user.

## 🚀 Features

- **Supervisor** – coordinates workflow and agent collaboration  
- **Coder** – generates and edits code  
- **Files** – handles reading, writing, and file management  
- **Research** – searches and collects information  
- **Answer** – assembles and formats the final response  
- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://github.com/langchain-ai/langgraph)  
- Modular design, easily extendable with new agents  

## 📦 Requirements

- Python **3.10+**
- Dependencies listed in `pyproject.toml` (can be installed with `uv`)

## 🔧 Installation

### 1. Install `uv`
```bash
pip install uv
```

### 2. Clone the repository
```bash
git clone https://github.com/KopatychDisko/Multi-Agent-AI-Orchestrator.git
cd Multi-Agent-AI-Orchestrator
```

### 3. Install dependencies
```bash
uv install
```

## ▶ Running the Project

To run the orchestrator from the console:
```bash
python main.py
```

## 📂 Project Structure
```
Multi-Agent-AI-Orchestrator/
├── agents/             # Agent implementations
├── main.py             # Entry point for console execution
├── agent.ipynb         # Notebook version
├── pyproject.toml      # Project dependencies
├── uv.lock             # Lock file for uv
└── README.md
```
