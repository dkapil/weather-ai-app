from openai import OpenAI
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def agent_step(user_input):
    prompt = f"""
You are an AI agent.

You can use the tool:
get_weather(city)

Respond ONLY in this format:

Thought: what you think
Action: get_weather(city_name)

Do NOT generate Observation.
Do NOT generate Final Answer.
If the input is ambiguous, ask a clarification question instead of taking arbitrary action.

User Input: {user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


def final_step(user_input, observation):
    prompt = f"""
You are an AI assistant.

Given the observation below, provide the final answer.

User Input: {user_input}
Observation: {observation}

Respond ONLY in this format:

Final Answer: <your answer>
Explain your reasoning briefly.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


def parse_action(text):
    match = re.search(r'get_weather\((.*?)\)', text)
    if match:
        return match.group(1).strip().strip('"').strip("'")
    return None