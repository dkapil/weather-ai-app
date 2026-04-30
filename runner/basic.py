from agents.basic import agent_step, final_step, parse_action
from tools.weather import get_weather

print("Agent starting...")

while True:
    user_input = input("Ask: ")
    if user_input.lower() == "exit":
        break

    # Step 1: LLM decides what to do
    step_output = agent_step(user_input)
    print(step_output)

    # Step 2: Extract action
    city = parse_action(step_output)

    if city:
        # Execute tool
        result = get_weather(city)
        print("Observation:", result)

        # Step 3: LLM generates final answer using real observation
        final_output = final_step(user_input, observation=result)
        print(final_output)
    else:
        print("No valid action found")
