from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.database.models import CropDisease
from modules.database.schemas.crop_disease_schemas import CropDiseaseCreate
from modules.utilities.auth import get_db_session

router = APIRouter(tags=["CropDiseases"])


@router.post("/crop_diseases/", response_model=CropDiseaseCreate)
def create_crop_disease(crop_disease: CropDiseaseCreate, db: Session = Depends(get_db_session)):  # noqa: B008
    # AI integration for crop disease detection
    # ai_response = requests.post("AI_API_URL", json=crop_disease.dict()).json()
    # Parse AI response and update the crop_disease object if needed
    db_crop_disease = CropDisease(**crop_disease.dict())
    db.add(db_crop_disease)
    db.commit()
    db.refresh(db_crop_disease)
    return db_crop_disease
