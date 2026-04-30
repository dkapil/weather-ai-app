from agents.multitool import agent_step, final_step, parse_action, is_valid_action
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

    # Step 4: Print final step_output (after retries)
    print(step_output)

    # Step 5: Parse action
    tool, arg = parse_action(step_output)

    if tool in TOOLS:
        # Step 6: Execute tool
        result = TOOLS[tool](arg)
        print("Observation:", result)

        # Step 7: Generate final answer
        final_output = final_step(user_input, result)
        print(final_output)

        # ✅ ONLY final answer goes into global history
        history.append({"role": "assistant", "content": final_output})

    else:
        # No action (clarification / refusal case)
        print("Agent could not determine action. Response:")
        print(step_output)
