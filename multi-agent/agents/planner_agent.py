from openai import OpenAI
from dotenv import load_dotenv
import os, json, httpx, urllib3

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http_client = httpx.Client(verify=False)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=http_client,
)


def create_plan(user_query: str):

    system_prompt = """
You are a planning agent.

Your ONLY job is to analyse the user query and decide:
1. Which tools are required
2. In what order they should be executed

Available tools:
- get_weather(city)
- get_air_quality(city)
- get_time(city)

IMPORTANT RULES:

- You MUST NOT answer the query
- You MUST NOT explain reasoning
- You MUST NOT generate observations
- You MUST ONLY generate structured JSON
- If the user explicitly mentions a city, do NOT ask for clarification

For queries related to:
- running
- exercise
- outdoor activity
- pollution
- breathing
→ prioritize air quality

For general outdoor comfort:
→ weather + air quality

For time-related queries:
→ get_time

If city is ambiguous:
→ ask clarification

If query is unrelated:
→ refuse

Output format (STRICT JSON ONLY)

PLAN FORMAT:
{
  "type": "plan",
  "tasks": [
    {
      "tool": "get_weather",
      "input": "Delhi"
    }
  ]
}

CLARIFICATION FORMAT:
{
  "type": "clarification",
  "message": "Which city are you referring to?"
}

REFUSAL FORMAT:
{
  "type": "refusal",
  "message": "I can only help with weather, time, and air quality queries."
}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
    )

    content = response.choices[0].message.content

    return json.loads(content)
