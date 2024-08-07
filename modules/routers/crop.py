from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.database.models import Crop
from modules.database.schemas.crop_schema import CropCreate
from modules.utilities.auth import get_db_session

router = APIRouter(tags=["crop"])

@router.post("/crop/", response_model=CropCreate)
def create_crop(crop: CropCreate, db: Session = Depends(get_db_session)):  # noqa: B008
    db_crop = Crop(crop_type=crop.crop_type, notes=crop.notes, planted_on=crop.planted_on, farm_id=crop.farm_id)
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop
