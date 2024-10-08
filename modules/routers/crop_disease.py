from typing import List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from modules.database.models.crop_diagnosis_models import CropDiagnosis
from modules.database.schemas.crop_diagnosis_schemas import (
    CropDiagnosisBase,
    CropDiagnosisCreate,
)
from modules.utilities.auth import get_db_session
from modules.utilities.gemini_integration import get_disease_data

router = APIRouter(tags=["CropDiseases"])


# @router.post("/crop_diseases/", response_model=CropDiseaseCreate)
# def create_crop_disease(crop_disease: CropDiseaseCreate, db: Session = Depends(get_db_session)):  # noqa: B008
#     # AI integration for crop disease detection
#     # ai_response = requests.post("AI_API_URL", json=crop_disease.dict()).json()
#     # Parse AI response and update the crop_disease object if needed
#     db_crop_disease = CropDisease(**crop_disease.dict())
#     db.add(db_crop_disease)
#     db.commit()
#     db.refresh(db_crop_disease)
#     return db_crop_disease


@router.post("/crop-diseases/detect", response_model=CropDiagnosisCreate)
async def detect_crop_disease(
    user_prompt: str, crop_id: int, files: List[UploadFile], db: Session = Depends(get_db_session)  # noqa: B008
):
    # async def detect_crop_disease(user_prompt: str, files: List[UploadFile] = File(...)):
    filePaths = []
    for file in files:
        file_location = f"uploaded_files/{file.filename}"
        filePaths.append(file_location)
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
    diagnosis, images = get_disease_data(user_prompt, filePaths)
    payload = {"crop_id": crop_id, "images": images, **diagnosis}
    db_crop_diagnosis = CropDiagnosis(**payload)
    db.add(db_crop_diagnosis)
    db.commit()
    db.refresh(db_crop_diagnosis)
    return db_crop_diagnosis


@router.post("/crop-diseases/generic", response_model=CropDiagnosisBase)
async def generic_detect_crop_disease(
    user_prompt: str, files: List[UploadFile], db: Session = Depends(get_db_session)  # noqa: B008
):
    """Delete a Farm instance."""

    filePaths = []
    for file in files:
        file_location = f"uploaded_files/{file.filename}"
        filePaths.append(file_location)
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
    diagnosis, images = get_disease_data(user_prompt, filePaths)
    payload = {"images": images, **diagnosis}
    return payload


@router.get("/crop-diseases/{crop_diagnosis_id}", response_model=CropDiagnosisCreate)
def get_crop_disease(crop_diagnosis_id: int, db: Session = Depends(get_db_session)):
    """Get a crop disease instance."""
    return db.query(CropDiagnosis).filter(CropDiagnosis.id == crop_diagnosis_id).first()


@router.get("/crop-diseases/history", response_model=List[CropDiagnosisCreate])
def get_crop_disease_history(crop_id: int, db: Session = Depends(get_db_session)):
    """Get a crop disease history."""
    return db.query(CropDiagnosis).filter(CropDiagnosis.crop_id == crop_id).all()
