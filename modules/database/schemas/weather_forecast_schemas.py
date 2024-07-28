from datetime import datetime

from pydantic import BaseModel


class WeatherForecastBase(BaseModel):
    date: datetime
    temperature: float
    humidity: float
    precipitation: float
    wind_speed: float
    forecast_type: str


class WeatherForecastCreate(WeatherForecastBase):
    farm_id: int


class WeatherForecastInDB(WeatherForecastBase):
    id: int
    farm_id: int
    created_at: datetime

    class Config:
        orm_mode = True
