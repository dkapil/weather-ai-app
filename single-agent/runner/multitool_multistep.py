import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.multitool_multistep_agent import (
    agent_step,
    final_step,
    parse_action,
    is_valid_action,
)

from tools.weather import get_weather
from tools.time import get_time
from tools.air_quality import get_air_quality

TOOLS = {
    "get_weather": get_weather,
    "get_time": get_time,
    "get_air_quality": get_air_quality,
}

print("Agent starting...")

history = [
    {
        "role": "system",
        "content": """
You are an intelligent agent that uses tools to answer user queries.

You have access to the following tools:
1. get_weather(city) → for weather information
2. get_time(city) → for current time
3. get_air_quality(city) → for pollution / air quality

Your job is to:
- understand the user's intent
- choose the MOST appropriate tool
- take action to retrieve the required information

You are a decision-making agent, not a conversational chatbot.

Rules:
- You MUST use a tool for any query related to:
  - weather
  - temperature
  - time
  - air quality
  - outdoor conditions (e.g., “should I go outside”, “do I need a jacket”)

- Do NOT answer directly if a tool can be used
- Use ONLY one tool at a time
- If the query is ambiguous, ask for clarification
- If completely unrelated, politely refuse

- For decision-making queries (e.g., "should I...", "is it a good time...", "is it safe..."):
  - Consider multiple relevant factors before answering
  - You may call multiple tools across steps if needed
  - Do not rely on a single factor if others are clearly relevant

- When working with air quality data:
  - Treat PM2.5 and PM10 as particulate matter measurements
  - Do NOT refer to PM2.5 or PM10 values as "AQI"
  - Only use the term "AQI" if it is explicitly present in the tool output

When specifying a city:
- Prefer well-known global cities
- If a city name is ambiguous, include country (e.g., "Delhi, India", "Paris, France")
- Avoid using short or ambiguous location names without context

Output format (STRICT):
Thought: <your reasoning>
Action: <tool_name>(city_name)

Where <tool_name> is one of:
- get_weather
- get_time
- get_air_quality

Do NOT:
- generate Observation
- generate Final Answer
- skip Thought or Action
- invent tools

You may take multiple steps.

After each Observation:
- You can either take another Action
- OR provide Final Answer

If you have enough information, respond with:

Thought: ...
Final Answer: <your answer>
""",
    }
]

MAX_RETRIES = 2

while True:
    user_input = input("Ask: ")

    if user_input.lower() == "exit":
        break

    # Step 1: Add user input to global history
    history.append({"role": "user", "content": user_input})

    # 🔥 IMPORTANT: Create local copy for reasoning (retry loop)
    retry_history = history.copy()

    # Step 2: First attempt
    step_output = agent_step(retry_history)

    retry_count = 0

    # Step 3: Retry loop (uses ONLY retry_history)
    while (
        "Action:" in step_output
        and not is_valid_action(step_output)
        and retry_count < MAX_RETRIES
    ):

        retry_history.append({"role": "assistant", "content": step_output})

        retry_history.append(
            {
                "role": "system",
                "content": """
Your previous response was invalid.

You MUST follow this format strictly:

Thought: ...
Action: <tool_name>(city_name)

Where <tool_name> is one of:
- get_weather
- get_time
- get_air_quality

Rules:
- Choose the MOST appropriate tool
- Do NOT skip Action
- Do NOT invent new tools
- Only fix the format. Do not change the original intent.
""",
            }
        )

        step_output = agent_step(retry_history)
        retry_count += 1

    MAX_STEPS = 5
    step_count = 0

    current_history = retry_history.copy()

    # Start loop with FIRST step_output (no extra LLM call)
    while step_count < MAX_STEPS:

        # Only call LLM AFTER first iteration
        if step_count > 0:
            step_output = agent_step(current_history)

        tool, arg = parse_action(step_output)

        # CASE 1: Final Answer → STOP
        if tool == "FINAL":
            print(step_output)  # already formatted

            history.append({"role": "assistant", "content": f"Final Answer: {arg}"})
            break

        # CASE 2: Tool call
        elif tool in TOOLS:
            print(step_output)
            result = TOOLS[tool](arg)
            print("Observation:", result)

            # Add reasoning step
            current_history.append({"role": "assistant", "content": step_output})

            # Add observation
            current_history.append(
                {"role": "system", "content": f"Observation: {result}"}
            )

        # CASE 3: Invalid
        else:
            print("Agent could not determine next step.")
            break

        step_count += 1
