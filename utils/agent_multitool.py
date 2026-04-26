from openai import OpenAI
import os
from dotenv import load_dotenv
import re
import httpx
import urllib3

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http_client = httpx.Client(verify=False)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client)


def agent_step(history):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        temperature=0
    )

    return response.choices[0].message.content

def final_step(user_input, observation):
    prompt = f"""
You are an assistant that provides answers based ONLY on the given observation.

You may receive:
- weather data
- time data
- air quality data
- OR an error message

Your job:
- Use the observation to generate a COMPLETE and helpful answer
- Always include relevant details (e.g., time, temperature, air quality values)
- Make the answer natural and user-friendly

CRITICAL RULES:
- Always prioritize the observation over any prior knowledge
- Do NOT assume real-world conditions (e.g., do NOT assume a city is polluted unless data shows it)
- Do NOT mislabel values (e.g., PM2.5 ≠ AQI unless explicitly given)
- Base your interpretation strictly on the provided data

Air quality guidance:
- Lower PM2.5 / PM10 values indicate cleaner air
- If values are low, clearly state that air quality is good or clean
- If values are high, indicate pollution appropriately

If observation contains an error:
- Clearly explain the issue to the user
- Suggest what they can do next (e.g., provide a valid city)

DO NOT:
- refuse the request
- ask for clarification
- mention tools or internal steps
- return partial answers (e.g., just city name)

STRICT:
- Your answer MUST be derived from the observation
- Do NOT ignore the observation
- Do NOT hallucinate missing data

User Input: {user_input}
Observation: {observation}

Respond in this format:
Final Answer: <your answer>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

def parse_action(text):
    match = re.search(r'Action:\s*(\w+)\((.*?)\)', text)
    if match:
        tool = match.group(1)
        arg = match.group(2).strip().strip('"').strip("'")
        return tool, arg
    return None, None

def is_valid_action(output: str) -> bool:
    return (
        "Action:" in output and
        (
            "get_weather(" in output or
            "get_time(" in output or
            "get_air_quality(" in output
        )
    )