import os
import requests

API_KEY = os.getenv("WEATHER_API_KEY")


def get_time(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

        resp = requests.get(url)

        # print("\n[DEBUG] TIME API:", resp.text)

        data = resp.json()

        # Validate response
        if "error" in data:
            return {"error": data["error"]["message"]}

        return {
            "city": data["location"]["name"],
            "time": data["location"]["localtime"],
            "timezone": data["location"]["tz_id"],
        }

    except Exception as e:
        return {"error": str(e)}
