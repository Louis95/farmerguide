from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from modules.database.models import Farm, User
from modules.database.schemas.weather_forecast_schemas import (
    DailyWeatherForecast,
    FarmWeatherForecastResponse,
)
from modules.utilities import auth, weather_service
from modules.utilities.auth import get_db_session

router = APIRouter(tags=["WeatherForcast"])


@router.get("/farm-weather-forecast", response_model=FarmWeatherForecastResponse)
def get_weather_forcast(
    db: Session = Depends(get_db_session),
    farm_id: int = Query(..., description="The ID of the farm to return weather forecast for"),
    days: int = Query(..., description="The number of days return weather forecast"),
    current_user: User = Depends(auth.get_current_user),
):
    """Returns the weather forcast for a particular farm."""
    # user_farm = (
    #     db.query(user_farm_models.user_farm)
    #     .filter(
    #         user_farm_models.user_farm.c.user_id == current_user.id,
    #         user_farm_models.user_farm.c.farm_id == farm_id,
    #     )
    #     .first()
    # )

    # if not user_farm:
    #     raise HTTPException(status_code=403, detail="You don't have access to this farm")

    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    weather_forecast = weather_service.get_weather_forecast(
        latitude=farm.latitude, longitude=farm.longitude, days=days
    )

    forecast_response = FarmWeatherForecastResponse(
        farm_name=farm.name,
        latitude=farm.latitude,
        longitude=farm.longitude,
        forecast=[DailyWeatherForecast(**forecast) for forecast in weather_forecast],
    )

    return forecast_response
