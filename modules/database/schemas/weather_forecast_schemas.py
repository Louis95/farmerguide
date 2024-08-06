from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class DailyWeatherForecast(BaseModel):
    date: datetime = Field(None, description="")
    temperature_high: float = Field(None, description="The high temperature")
    temperature_low: float = Field(None, description="The low temperature")
    precipitation: float
    humidity: float
    wind_speed: float
    description: str = Field(None, description="The description")


class FarmWeatherForecastResponse(BaseModel):
    farm_name: str
    location: str
    forecast: List[DailyWeatherForecast]


class WeatherForecastInDB(DailyWeatherForecast):
    id: int
    farm_id: int
    created_at: datetime

    class Config:
        from_attributes = True
