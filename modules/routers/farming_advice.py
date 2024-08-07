from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.database.models import Crop, FarmingAdvice, WeatherForecast
from modules.database.schemas.farming_advice_schemas import FarmingAdviceCreate
from modules.utilities.auth import get_db_session
from modules.utilities.gemini_integration import get_advice_for_crop

router = APIRouter(tags=["FarmingAdvice"])


@router.post("/farming_advice/", response_model=FarmingAdviceCreate)
def create_farming_advice(advice: FarmingAdviceCreate, db: Session = Depends(get_db_session)):  # noqa: B008
    # AI integration for farming advice
    # ai_response = requests.post("AI_API_URL", json=advice.dict()).json()
    # Parse AI response and update the advice object if needed
    db_advice = FarmingAdvice(**advice.dict())
    db.add(db_advice)
    db.commit()
    db.refresh(db_advice)
    return db_advice


@router.get("/farming_advice/{advice_id}")
def get_farming_advice(advice_id: int, db: Session = Depends(get_db_session)):  # noqa: B008
    return db.query(FarmingAdvice).filter(FarmingAdvice.id == advice_id).first()


@router.get("/farming_advice")
def get_farming_advices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):  # noqa: B008
    return db.query(FarmingAdvice).offset(skip).limit(limit).all()


# get farming advise for a crop
@router.get("/farming_advice/crop/{crop_id}")
def get_farming_advices_for_crop(crop_id: int, db: Session = Depends(get_db_session)):  # noqa: B008
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        return None
    weather = (
        db.query(WeatherForecast)
        .filter(WeatherForecast.farm_id == crop.farm_id)
        .filter(WeatherForecast.date > datetime.now())
        .all()
    )
    # return crop
    crop_advise =  get_advice_for_crop(crop, weather)
    ## store the advise on the database
    return crop_advise
