import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["WEATHER_API_KEY"]


def get_weather_forecast(latitude, longitude, days):
    url = "https://api.openweathermap.org/data/2.5/forecast/daily"

    params = {"lat": latitude, "lon": longitude, "units": "metric", "cnt": days, "appid": api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    weather_data = response.json()

    forecasts = []

    for day in weather_data["list"]:
        forecast = {
            "date": datetime.fromtimestamp(day["dt"]),
            "temperature_high": day["temp"]["max"],
            "temperature_low": day["temp"]["min"],
            "humidity": day["humidity"],
            "precipitation": day.get("rain", 0),  # Default to 0 if 'rain' key is not present
            "wind_speed": day["speed"],
            "forecast_type": day["weather"][0]["description"],
        }
        forecasts.append(forecast)

    return forecasts
