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
- Base your interpretation strictly on the provided data

Air quality guidance:
- Lower PM2.5 / PM10 values indicate cleaner air
- If values are low, clearly state that air quality is good or clean
- If values are high, indicate pollution appropriately
- Do NOT refer to PM2.5 or PM10 values as "AQI"
- Only use the term "AQI" if it is explicitly present in the observation
- If only PM2.5 / PM10 values are provided, describe them correctly as particulate matter levels

If observation contains an error:
- Clearly explain the issue to the user
- Suggest what they can do next (e.g., provide a valid city)

When comparing or making decisions:
- Include key values used in reasoning (e.g., temperatures, PM2.5 / PM10 values)
- Briefly explain the reasoning behind the answer

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
        temperature=0.3,
    )

    return response.choices[0].message.content


def parse_action(text):
    # Check for action
    action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", text)
    if action_match:
        tool = action_match.group(1)
        arg = action_match.group(2).strip().strip('"').strip("'")
        return tool, arg    

    clarify_match = re.search(r"Clarify:\s*(.*)", text)
    if clarify_match:
        return "CLARIFY", clarify_match.group(1).strip()

    # Check for final action
    final_match = re.search(r"Final Answer:\s*(.*)", text, re.DOTALL)
    if final_match:
        return "FINAL", final_match.group(1).strip()

    return None, None


def is_valid_action(output: str) -> bool:
    return "Action:" in output and (
        "get_weather(" in output
        or "get_time(" in output
        or "get_air_quality(" in output
    )

def should_reflect(step_output: str, step_count: int) -> bool:
    if step_output is None:
        return True
    
    # weak signals of failure
    failure_patterns = [
        "I don't know",
        "cannot determine",
        "no tool",
        "unable to"
    ]

    if any(p in step_output.lower() for p in failure_patterns):
        return True
    
    # too many steps without final answer
    if step_count >= 1 and "Final Answer:" not in step_output:
        return True
    
    return False

def reflect(history, user_input):
    prompt = f"""
You are a self-reflective AI agent.

The previous steps did NOT successfully solve the user query.

User Query:
{user_input}

Conversation so far:
{history}

Your task:

1. Check whether the previous reasoning gathered ALL relevant information required to answer the user query.

2. If any important factor is missing (e.g., weather, air quality, time):
   - Identify what is missing
   - Explain why it is required
   - Call the appropriate tool

3. If ALL relevant information is already gathered:
   - DO NOT improve the explanation
   - DO NOT rewrite or expand the answer
   - Return Final Answer directly

IMPORTANT:

- Prioritize COMPLETENESS over explanation quality
- You are NOT responsible for improving explanation clarity or wording
- You are ONLY responsible for checking whether required data is missing

- For outdoor / safety / activity decisions:
    - Identify which factors are MOST relevant to the user query

- Air quality is critical for:
  - running, exercise, breathing, health concerns

- Identify the PRIMARY factor for the query:
  - Running / exercise → air quality is PRIMARY
  - General outdoor comfort → both weather and air quality may be relevant

- If equivalent data is already available (e.g., PM2.5 / PM10 instead of AQI), do NOT call the tool again

- Time is NOT required for outdoor safety decisions unless explicitly asked

Rules:

- Do NOT fetch additional data if the PRIMARY factor alone is sufficient to answer the question
- Only fetch secondary factors if they would significantly change the decision
- Do NOT call a tool if the existing data is already sufficient
- Do NOT repeat the same tool
- Do NOT critique explanation quality, wording, or clarity
- Do NOT add extra explanation
- Be concise
- Prefer calling a missing tool ONLY if needed

Output format (STRICT):

IF missing information:

Critique: <what is missing and why>
Action: <tool_name>(city)

IF information is sufficient:

Final Answer: <answer>
"""

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [{"role":"user", "content":prompt}],
        temperature = 0
    )

    return response.choices[0].message.content