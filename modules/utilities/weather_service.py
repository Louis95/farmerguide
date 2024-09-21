import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["WEATHER_API_KEY"]


def get_weather_forecast(latitude, longitude, days):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    # url = "https://api.openweathermap.org/data/2.5/forecast/daily"

    params = {"lat": latitude, "lon": longitude, "units": "metric", "cnt": days, "appid": api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    weather_data = response.json()

    forecasts = []

    for day in weather_data["list"]:
        forecast = {
            "date": datetime.fromtimestamp(day["dt"]),
            "temperature_high": day["main"]["temp_min"],
            "temperature_low": day["main"]["temp_max"],
            "humidity": day["main"]["humidity"],
            "precipitation": day.get("rain", 0),  # Default to 0 if 'rain' key is not present
            "wind_speed": day["wind"]["speed"],
            "forecast_type": day["weather"][0]["description"],
        }
        forecasts.append(forecast)

    return forecasts
def get_weather_forecast_by_timestamp(latitude, longitude, timestamp):
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

    params = {"lat": latitude, "lon": longitude, "units": "metric", "dt": timestamp, "appid": api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    weather_data = response.json()

    forecasts = []

    for day in weather_data["data"]:
        forecast = {
            "date": datetime.fromtimestamp(day["dt"]),
            "temperature": day["temp"],
            "pressure": day["pressure"],
            "humidity": day["humidity"],
            "wind_deg": day["wind_deg"],
            "dew_point": day["dew_point"],
            "wind_speed": day["speed"],
            "visibility": day["visibility"],
            "feels_like": day["feels_like"],
            "forecast_type": day["weather"],
        }
        forecasts.append(forecast)

    return forecasts
