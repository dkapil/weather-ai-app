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

## 🧩 Architecture Overview

```text
User Input
   ↓
Agent (LLM)
   ↓
Thought → Action
   ↓
Tool Execution
   ↓
Observation
   ↓
Final Answer (via LLM)
```

---

## 🛠️ Tools

| Tool                    | Description               |
| ----------------------- | ------------------------- |
| `get_weather(city)`     | Fetch current weather     |
| `get_time(city)`        | Fetch local time          |
| `get_air_quality(city)` | Fetch air quality metrics |

---

## 📁 Project Structure

```text
.
├── mainagent_multitool.py   # Main loop (agent execution)
├── utils/
│   └── agent_multitool.py  # LLM interaction, parsing, validation
├── tools/
│   ├── weather.py
│   ├── time.py
│   └── air_quality.py
├── .env                     # API keys
└── README.md
```
---

## 🧪 Agent Variants (Evolution of the System)

This repository contains multiple versions of the agent, capturing the step-by-step evolution from a simple LLM to a tool-using agent.

### 📂 Variants Overview

| File                       | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| `mainllm.py`               | Basic LLM interaction (no tools, no agent logic)       |
| `mainagent.py`             | Introduction to agent pattern (LLM + basic tool usage) |
| `mainagenthistory.py`      | Agent with conversation memory (context-aware)         |
| `mainagenthistoryretry.py` | Adds retry mechanism for invalid LLM outputs           |
| `mainagent_multitool.py`   | Current version: multi-tool agent (weather, time, AQI) |

---

### 🧠 Evolution Journey

```text id="evolution_flow"
LLM → Agent → Agent + Memory → Agent + Retry → Multi-Tool Agent
```

---

### 🔍 Why multiple versions?

Each version isolates a key concept:

* **`mainllm.py`** → Understand raw LLM behavior
* **`mainagent.py`** → Introduce Thought/Action pattern
* **`mainagenthistory.py`** → Add memory (state)
* **`mainagenthistoryretry.py`** → Add robustness (retry/validation)
* **`mainagent_multitool.py`** → Scale to multiple tools
---

### 🎯 Recommended Entry Point

If you're exploring the project:

* Start with → `mainllm.py`
* Then → `mainagent.py`
* Finally → `mainagent_multitool.py` (latest)

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
python mainagent_multitool.py
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
---
## 🙌 Contributions

Open to improvements, ideas, and experiments.
