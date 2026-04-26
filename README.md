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
