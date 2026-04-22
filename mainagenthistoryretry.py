from utils.historyagentwithretry import agent_step, final_step, parse_action, is_valid_action
from tools.weather import get_weather

print("Agent starting...")

history = [
    {
        "role": "system",
        "content": """
You are a weather assistant.

You can use the tool:
get_weather(city)

Rules:
- You primarily handle weather-related queries.
- If a query can be answered using weather data, interpret and proceed.
- If completely unrelated, politely refuse.

- If reasonably confident, proceed with best guess.
- Ask clarification only if necessary.

- Respond ONLY in this format when taking action:
  Thought: ...
  Action: get_weather(city_name)

- Do NOT generate Observation
- Do NOT generate Final Answer here
"""
    }
]

MAX_RETRIES = 2

while True:
    user_input = input("Ask: ")

    if user_input.lower() == "exit":
        break

    # Step 1: Add user input to the history
    history.append({
        "role": "user", 
        "content" : user_input
    })

    # Step 2: LLM decides action
    step_output = agent_step(history)

    retry_count = 0

    # Step 3: Retry if invalid action
    while "Action:" in step_output and not is_valid_action(step_output) and retry_count < MAX_RETRIES:
        history.append({
                "role": "system",
                "content": """
Your previous response was invalid.

You MUST follow this format strictly:
Thought: ...
Action: get_weather(city_name)

Do NOT skip Action.
"""
        })

        step_output = agent_step(history)
        retry_count += 1
    
    print(step_output)

    # Step 3: Add LLM response to memory
    history.append({
        "role" : "assistant",
        "content" : step_output
    })

    # Step 4: Parse action
    city = parse_action(step_output)

    if city:
        # Step 5: Execute tool
        result = get_weather(city)
        print("Observation:", result)

        # Step 6: Generate final answer using real observation
        final_output=final_step(user_input,result)
        print(final_output)

        # Step 7: Add final answer to memory
        history.append({
            "role" : "assistant",
            "content" : final_output
        })
    else:
        #print("No valid action found")
        pass