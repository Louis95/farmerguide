from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.database.models import SoilHealth
from modules.database.schemas.soil_health_schemas import SoilHealthCreate
from modules.utilities.auth import get_db_session

router = APIRouter(tags=["SoilHealth"])


@router.post("/soil_health/", response_model=SoilHealthCreate)
def create_soil_health(soil_health: SoilHealthCreate, db: Session = Depends(get_db_session)):  # noqa: B008
    # AI integration for soil health analysis
    # ai_response = requests.post("AI_API_URL", json=soil_health.dict()).json()
    # Parse AI response and update the soil_health object if needed
    db_soil_health = SoilHealth(**soil_health.dict())
    db.add(db_soil_health)
    db.commit()
    db.refresh(db_soil_health)
    return db_soil_health
