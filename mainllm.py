from utils.llm import extract_city
from tools.weather import get_weather

print("Agent starting...")

while True:
    user_input = input("Ask: ")
    if user_input.lower() == "exit":
        break

    # TEMP: naive extraction
    city = extract_city(user_input)

    result = get_weather(city)

    print(result)
