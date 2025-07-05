# mcp_tool.py
import requests

def get_weather(city: str) -> str:
    geo_resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city}
    ).json()

    if "results" not in geo_resp:
        return f"❌ Could not find location '{city}'."

    loc = geo_resp["results"][0]
    lat, lon, city_name = loc["latitude"], loc["longitude"], loc["name"]

    weather_resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True}
    ).json()

    if "current_weather" not in weather_resp:
        return f"⚠️ Weather unavailable for {city_name}."

    weather = weather_resp["current_weather"]
    return f"🌤️ {city_name}: {weather['temperature']}°C, Windspeed: {weather['windspeed']} km/h"
