# Weather AI Agent (ReAct-based Multi-Tool Agent)

A simple but powerful **agentic AI system** built using the **ReAct pattern**, capable of reasoning, selecting tools, and responding using real-world data.

---

## 🚀 Features

* 🔁 **ReAct-style reasoning (Thought → Action → Observation)**
* 🧰 **Multi-tool support**

  * Weather
  * Time
  * Air Quality
* 🌐 **Real API integrations**
* 🧠 **Context-aware (conversation memory)**
* 🛡️ **Guardrails for tool usage**
* 🔄 **Retry mechanism for malformed outputs**

---

## 🛠️ Tools

| Tool                    | Description               |
| ----------------------- | ------------------------- |
| `get_weather(city)`     | Fetch current weather     |
| `get_time(city)`        | Fetch local time          |
| `get_air_quality(city)` | Fetch air quality metrics |

---

## 🧪 Agent Variants (Evolution of the System)

This repository contains multiple agent variants, capturing the step-by-step evolution from a simple LLM to a multi-step ReAct agent.

### 📂 Variants Overview

| File                                  | Description                              |
| ------------------------------------- | ---------------------------------------- |
| `mainllm.py`                          | Basic LLM interaction (no tools)         |
| `basic_agent.py`                      | First agent with single tool usage       |
| `history_agent.py`                    | Adds conversation memory                 |
| `history_retry_agent.py`              | Adds retry mechanism for invalid outputs |
| `multitool_agent.py`                  | Supports multiple tools                  |
| `multitool_multistep_agent.py`        | Final multi-step ReAct agent          |

---

### 🧠 Evolution Journey

```text id="evolution_flow"
LLM → Agent → Memory → Retry → Multi-Tool → Multi-Step (ReAct)
```

---

### 🔍 Why multiple versions?

Each variant isolates a key concept:

* **`mainllm.py`** → Raw LLM behavior
* **`basic_agent.py`** → Thought/Action pattern
* **`history_agent.py`** → Memory (state)
* **`history_retry_agent.py`** → Robustness (retry/validation)
* **`multitool_agent.py`** → Tool selection across multiple tools
* **`multitool_multistep_agent.py`** → Iterative reasoning + multi-step execution

---

### 🎯 Recommended Entry Point

If you're exploring the project:

* Start with → `mainllm.py`
* Then → `basic_agent.py`
* Finally → `multitool_multistep_agent.py` (latest)

---

### ⚠️ Note

Older variants are intentionally kept for learning purposes and may not include the latest improvements.

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone <your-repo-url>
cd weather-ai-agent
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install openai python-dotenv requests httpx
```

### 4. Add environment variables

Create `.env` file:

```env
OPENAI_API_KEY=your_openai_key
WEATHERAPI_KEY=your_weatherapi_key
TIMEZONEDB_API_KEY=your_timezonedb_key
```

---

## ▶️ Run the Agent

```bash
python multitool_multistep_agent.py
```

---

## 🧪 Example Queries

```text
weather in london
time in tokyo
air quality in delhi

is delhi polluted
do i need a jacket in tokyo
should I go outside in delhi
```
