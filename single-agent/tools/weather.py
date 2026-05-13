import requests
import os
from dotenv import load_dotenv
from utils.location import normalize_city

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city):
    city = normalize_city(city)
    url = "http://api.weatherapi.com/v1/current.json"

    params = {"key": API_KEY, "q": city}

    try:
        response = requests.get(url, params=params, timeout=3, verify=False)

        if response.status_code != 200:
            print("FULL RESPONSE:", response.text)
            return {"error": f"API error: {response.status_code}"}

        data = response.json()

        return {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "weather": data["current"]["condition"]["text"],
        }

    except Exception as e:
        return {"error": str(e)}
