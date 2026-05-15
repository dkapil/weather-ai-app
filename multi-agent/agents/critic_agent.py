from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import httpx
import urllib3

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http_client = httpx.Client(verify=False)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client)


def review(query, observations):

    system_prompt = """
You are a critic agent.

Your ONLY responsibilities are:
1. Review the available observations
2. Decide whether the information is sufficient
3. Generate a final answer

IMPORTANT RULES:

- You MUST NOT invent missing data
- You MUST NOT assume weather or air quality values
- Use ONLY the provided observations

Decision policies:

1. Running / exercise / breathing-related queries:
   - Air quality is the PRIMARY factor
   - Air quality alone is usually sufficient
   - Weather is secondary unless explicitly requested

2. General outdoor comfort queries:
   - Both weather and air quality are important

3. Time-related queries:
   - Time information alone is sufficient

If observations are sufficient:
Return:

{
  "status": "complete",
  "answer": "..."
}

If observations are NOT sufficient:
Return:

{
  "status": "incomplete",
  "reason": "Missing weather information"
}

STRICT:
- Output JSON ONLY
- No explanations
- No markdown
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"""
Query:
{query}

Observations:
{json.dumps(observations)}
""",
            },
        ],
    )

    content = response.choices[0].message.content

    return json.loads(content)
