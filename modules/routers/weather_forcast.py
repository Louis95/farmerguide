from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.database.models import WeatherForecast
from modules.database.schemas.weather_forecast_schemas import WeatherForecastCreate
from modules.utilities.auth import get_db_session

router = APIRouter(tags=["WeatherForcast"])


@router.post("/weather_forcast/", response_model=WeatherForecastCreate)
def create_weather_forcast(
    weather_forcast: WeatherForecastCreate, db: Session = Depends(get_db_session)  # noqa: B008
):  # noqa: B008
    # AI integration for crop disease detection
    # ai_response = requests.post("AI_API_URL", json=crop_disease.dict()).json()
    # Parse AI response and update the crop_disease object if needed
    db_weather_forcast = WeatherForecast(**weather_forcast.dict())
    db.add(weather_forcast)
    db.commit()
    db.refresh(weather_forcast)
    return db_weather_forcast
