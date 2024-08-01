from typing import List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from modules.database.models import CropDisease
from modules.database.models.crop_diagnosis_models import CropDiagnosis
from modules.database.schemas.crop_diagnosis_schemas import CropDiagnosisCreate
from modules.database.schemas.crop_disease_schemas import CropDiseaseCreate
from modules.utilities.auth import get_db_session
from modules.utilities.gemini_integration import get_disease_data

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


@router.post("/crop-diseases/detect", response_model=CropDiagnosisCreate)
async def detect_crop_disease(
    user_prompt: str, farm_id: int, files: List[UploadFile], db: Session = Depends(get_db_session)  # noqa: B008
):
    # async def detect_crop_disease(user_prompt: str, files: List[UploadFile] = File(...)):
    filePaths = []
    for file in files:
        file_location = f"uploaded_files/{file.filename}"
        filePaths.append(file_location)
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
    diagnosis, images = get_disease_data(user_prompt, filePaths)
    payload = {"farm_id": farm_id, "images": images, **diagnosis}
    db_crop_diagnosis = CropDiagnosis(**payload)
    db.add(db_crop_diagnosis)
    db.commit()
    db.refresh(db_crop_diagnosis)
    return db_crop_diagnosis
@router.get("/crop-diseases/{crop_diagnosis_id}", response_model=CropDiagnosisCreate)
def get_crop_disease(crop_diagnosis_id: int, db: Session = Depends(get_db_session)):
    return db.query(CropDiagnosis).filter(CropDiagnosis.id == crop_diagnosis_id).first()

@router.get("/crop-diseases/history", response_model=List[CropDiagnosisCreate])
def get_crop_disease_history(farm_id: int, db: Session = Depends(get_db_session)):
    return db.query(CropDiagnosis).filter(CropDiagnosis.farm_id == farm_id).all()