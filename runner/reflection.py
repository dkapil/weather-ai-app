import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.reflection_agent import (
    agent_step,
    final_step,
    parse_action,
    is_valid_action,
    should_reflect,
    reflect
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

- You MUST ALWAYS call a tool before answering any query related to:
  - weather
  - air quality
  - outdoor activities (including running, exercise, going outside)

- Even if you think you already know the answer, you are NOT allowed to answer without calling a tool first

- Use ONLY one tool at a time
- If the query is ambiguous, ask for clarification
- If completely unrelated, politely refuse

- If you realize that your previous reasoning was incomplete or incorrect:
  - You may revise your approach
  - You may choose a different tool
  - You should NOT repeat the same action again

- Avoid loops:
  - Do NOT call the same tool with the same input repeatedly

- For decision-making queries:
  - You may use a tool to answer
  - You are allowed to answer after a single tool if you think it is sufficient

- When working with air quality data:
  - Treat PM2.5 and PM10 as particulate matter measurements
  - Do NOT refer to PM2.5 or PM10 values as "AQI"
  - Only use the term "AQI" if it is explicitly present in the tool output
  - Interpret particulate matter correctly:
    - High PM2.5 (>75) or PM10 (>150) indicates poor air quality
    - Consider BOTH PM2.5 and PM10 when evaluating pollution levels
    - Do NOT assume air quality is moderate or safe if either value is high
  - If PM2.5 and PM10 values are already available:
    - Do NOT attempt to fetch AQI again
    - These values are sufficient to assess air quality

When specifying a city:
- Prefer well-known global cities
- If a city name is ambiguous, include country (e.g., "Delhi, India", "Paris, France")
- Avoid using short or ambiguous location names without context

Output format (STRICT):
Thought: <your reasoning>

EITHER:
Action: <tool_name>(city_name)

OR:
Clarify: <question to user>

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

    reflection_used = False

    # ADD this before loop
    tool_cache = {}

    # Start loop with FIRST step_output (no extra LLM call)
    while step_count < MAX_STEPS:

        if step_count > 0:
            step_output = agent_step(current_history)

        tool, arg = parse_action(step_output)

        # =========================
        # CASE 1: FINAL ANSWER
        # =========================
        if tool == "FINAL":

            if step_count == 0:
                print("Forcing tool usage before answering...")

                # fallback action (air quality is safest default for outdoor queries)
                step_output = f"""
        Thought: I must use a tool before answering this query.
        Action: <tool_name>(city_name)
        """
                continue

            # 🔥 REFLECTION FIRST
            if not reflection_used and step_count >= 1:
                print("Triggering Reflexion (post-final)...")

                reflection_output = reflect(current_history, user_input)
                print("Reflection triggered")

                tool_check, arg_check = parse_action(reflection_output)

                # CASE 1: reflection returns FINAL → STOP IMMEDIATELY
                if tool_check == "FINAL":

                    # ENFORCE tool usage for domain queries
                    if step_count == 0:
                        print("Forcing tool usage before answering...")

                        # inject forced step
                        step_output = f"""
                    Thought: I must use a tool before answering this query.
                    Action: <tool_name>(city_name)
                    """
                        continue

                    print(reflection_output)

                    history.append({
                        "role": "assistant",
                        "content": f"Final Answer: {arg_check}"
                    })

                    break  # HARD STOP

                # 🔥 CASE 2: reflection returns ACTION → continue loop
                elif tool_check in TOOLS:
                    current_history.append({
                        "role": "assistant",
                        "content": reflection_output
                    })

                    step_output = reflection_output
                    reflection_used = True
                    continue

                else:
                    print("Invalid reflection output. Skipping reflection.")
                    continue

            # 🔥 ACCEPT ORIGINAL FINAL
            print(step_output)

            history.append({
                "role": "assistant",
                "content": f"Final Answer: {arg}"
            })

            break  # 🔥 HARD STOP

        # =========================
        # CASE 2: TOOL CALL
        # =========================
        elif tool in TOOLS:

            key = f"{tool}:{arg}"

            # CACHE FIX
            if key in tool_cache:
                print(f"Reusing cached result for {tool}({arg})")
                result = tool_cache[key]
            else:
                print(step_output)
                result = TOOLS[tool](arg)
                tool_cache[key] = result
                print("Observation:", result)

            current_history.append({
                "role": "assistant",
                "content": step_output
            })

            current_history.append(
                {"role": "system", "content": f"Observation: {result}"}
            )


        # =========================
        # CASE 3: CLARIFY
        # =========================
        elif tool == "CLARIFY":
            print(f"Clarification needed: {arg}")

            history.append({
                "role": "assistant",
                "content": arg
            })

            break


        # =========================
        # CASE 4: INVALID
        # =========================
        else:
            print("Final Answer: I can only help with weather, time, and air quality related questions. Please ask something within this scope.")

            history.append({
                "role": "assistant",
                "content": "Final Answer: Out of scope"
            })

            break

        step_count += 1


    # CRITICAL: HARD STOP after FINAL / CLARIFY / INVALID
    continue
