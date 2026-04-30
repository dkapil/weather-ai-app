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
        model="gpt-4o-mini", messages=history, temperature=0
    )

    return response.choices[0].message.content


def final_step(user_input, observation):
    prompt = f"""
You are a weather assistant.

The weather data has already been fetched using a tool.

Your job is to answer the user based ONLY on the observation below.

DO NOT:
- refuse the request
- ask clarification
- mention tools

ONLY provide the final answer.

User Input: {user_input}
Observation: {observation}

Respond in this format:
Final Answer: <your answer>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content


def parse_action(text):
    match = re.search(r"get_weather\((.*?)\)", text)
    if match:
        return match.group(1).strip().strip('"').strip("'")
    return None


def is_valid_action(output: str) -> bool:
    return "Action:" in output and "get_weather(" in output
