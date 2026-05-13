import os
import requests
from utils.location import normalize_city

API_KEY = os.getenv("WEATHER_API_KEY")


def get_air_quality(city):
    try:
        city = normalize_city(city)
        url = (
            f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes"
        )

        resp = requests.get(url)

        # print("\n[DEBUG] AQI API:", resp.text)

        data = resp.json()

        if "error" in data:
            return {"error": data["error"]["message"]}

        aqi_data = data["current"]["air_quality"]

        return {
            "city": data["location"]["name"],
            "aqi_pm2_5": aqi_data.get("pm2_5"),
            "aqi_pm10": aqi_data.get("pm10"),
            "co": aqi_data.get("co"),
        }

    except Exception as e:
        return {"error": str(e)}
