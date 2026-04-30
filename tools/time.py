import os
import requests
from utils.location import normalize_city

API_KEY = os.getenv("WEATHER_API_KEY")


def get_time(city):
    try:
        city = normalize_city(city)
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

        resp = requests.get(url)

        print("\n[DEBUG] TIME API:", resp.text)

        data = resp.json()

        # Validate response
        if "error" in data:
            return {"error": data["error"]["message"]}

        return {
            "city": data["location"]["name"],
            "time": data["location"]["localtime"].split(" ")[1],
            "date": data["location"]["localtime"].split(" ")[0],
            "timezone": data["location"]["tz_id"],
        }

    except Exception as e:
        return {"error": str(e)}
