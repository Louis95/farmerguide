from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from modules.database.models import Crop, Farm, User
from modules.database.schemas.crop_schema import CropCreate, CropResponse, CropUpdate
from modules.utilities.auth import get_current_user, get_db_session

router = APIRouter(tags=["crop"])


@router.post("/crops", status_code=status.HTTP_201_CREATED, response_model=CropResponse)
def create_crop(
    crop: CropCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):  # noqa: B008
    """Create a new crop record."""
    db_farm = db.query(Farm).filter_by(id=crop.farm_id).first()

    if not db_farm:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No farm with that id")

    db_crop = Crop(
        crop_type=crop.crop_type, notes=crop.notes, planted_on=crop.planted_on, farm_id=crop.farm_id
    )  # noqa: B950
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop


@router.get("/crops", response_model=List[CropResponse])
def get_crops(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    """Retrieve all crops."""
    return db.query(Crop).all()


@router.get("/crops/{crop_id}", response_model=CropResponse)
def get_crop(
    crop_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)
):  # noqa: B950
    """Retrieve a specific crop by its ID."""
    db_crop = db.query(Crop).filter_by(id=crop_id).first()
    if not db_crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    return db_crop


@router.put("/crops/{crop_id}", response_model=CropResponse)
def update_crop(
    crop_id: int,
    crop: CropUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Update an existing crop record."""
    db_crop = db.query(Crop).filter(Crop.id == crop_id).first()

    if not db_crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    db_crop.crop_type = crop.crop_type
    db_crop.notes = crop.notes
    db_crop.planted_on = crop.planted_on

    db.commit()
    db.refresh(db_crop)

    return db_crop


@router.delete("/crops/{crop_id}")
def delete_crop(
    crop_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)
):  # noqa: B950
    """Delete a crop record."""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()

    if not crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    db.delete(crop)
    db.commit()

    return {"message": "Crop deleted"}
