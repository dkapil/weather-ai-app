from openai import OpenAI
import os
from dotenv import load_dotenv
import httpx
import urllib3

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http_client = httpx.Client(verify=False)

print("CWD:", os.getcwd())
print("ENV:", os.getenv("OPENAI_API_KEY"))
print("API KEY:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client)


def extract_city(user_input):
    prompt = f"""
Extract the city name from the input.
Return ONLY the city name. No extra words.

Input: {user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()
