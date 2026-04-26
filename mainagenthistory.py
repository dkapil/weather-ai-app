from utils.historyagent import agent_step, final_step, parse_action
from tools.weather import get_weather

print("Agent starting...")

history = [
    {
        "role": "system",
        "content": """
You are a weather assistant.

You ONLY handle queries related to weather.

You can use the tool:
get_weather(city)

Rules:
- If the query is NOT related to weather, politely refuse.
- Do NOT answer general knowledge questions.
- Do NOT guess outside your domain.
- Respond ONLY in this format:
  Thought: ...
  Action: get_weather(city_name)
- Do NOT generate Observation
- Do NOT generate Final Answer
- If input is ambiguous, ask a clarification question instead of guessing
""",
    }
]


while True:
    user_input = input("Ask: ")

    if user_input.lower() == "exit":
        break

    # Step 1: Add user input to the history
    history.append({"role": "user", "content": user_input})

    # Step 2: LLM decides action
    step_output = agent_step(history)
    print(step_output)

    # Step 3: Add LLM response to memory
    history.append({"role": "assistant", "content": step_output})

    # Step 4: Parse action
    city = parse_action(step_output)

    if city:
        # Step 5: Execute tool
        result = get_weather(city)
        print("Observation:", result)

        # Step 6: Generate final answer using real observation
        final_output = final_step(user_input, result)
        print(final_output)

        # Step 7: Add final answer to memory
        history.append({"role": "assistant", "content": final_output})
    else:
        # print("No valid action found")
        pass
