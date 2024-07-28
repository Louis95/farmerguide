from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.database.models import FarmingAdvice
from modules.database.schemas.farming_advice_schemas import FarmingAdviceCreate
from modules.utilities.auth import get_db_session

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
