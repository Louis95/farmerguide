from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from modules.database.models import Crop
from modules.database.models.farm_advice_models import FarmingAdvice
from modules.database.schemas.farming_advice_schemas import FarmingAdviceResponse
from modules.utilities import weather_service
from modules.utilities.auth import get_db_session
from modules.utilities.gemini_integration import get_advice_for_crop

router = APIRouter(tags=["FarmingAdvice"])


@router.get("/farming_advice/{advice_id}")
def get_farming_advice(advice_id: int, db: Session = Depends(get_db_session)):  # noqa: B008
    return db.query(FarmingAdvice).filter(FarmingAdvice.id == advice_id).first()


# get farming advise for a crop
@router.get("/farming_advice/crop/{crop_id}", response_model=FarmingAdviceResponse)
def get_farming_advices_for_crop(
    crop_id: int,
    days: int = Query(..., description="The number of days return weather forecast"),
    db: Session = Depends(get_db_session),
):  # noqa: B008
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        return None
    # Check if there exist an advise for this crop for today using day from timestamp and if there is one already generated return it
    # otherwise query the gemini api.
    #  This will help to avoid generating the same advise multiple times for the same on the same day
    #  and also reduce the number of requests to the gemini api

    today = datetime.now().date()
    advice = (
        db.query(FarmingAdvice).filter(FarmingAdvice.crop_id == crop_id, FarmingAdvice.created_at >= today).first()
    )
    if advice:
        return advice

    weather_forecast = weather_service.get_weather_forecast(
        latitude=crop.farm.latitude, longitude=crop.farm.longitude, days=days
    )
    crop_advise = get_advice_for_crop(crop, weather_forecast)

    # Store the advise on the database
    db_advice = FarmingAdvice(
        crop_id=crop.id,
        advice_type=crop_advise["advice_type"],
        advice=crop_advise["advice"],
        other_things_to_note=crop_advise["other_things_to_note"],
        duration=crop_advise["duration"],
    )
    db.add(db_advice)
    db.commit()
    db.refresh(db_advice)

    return crop_advise
