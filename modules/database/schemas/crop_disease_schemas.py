from datetime import datetime

from pydantic import BaseModel


class CropDiseaseBase(BaseModel):
    crop_type: str
    disease_name: str
    confidence: float
    image_url: str
    treatment_recommendation: str


class CropDiseaseCreate(CropDiseaseBase):
    farm_id: int


class CropDiseaseInDB(CropDiseaseBase):
    id: int
    farm_id: int
    detected_at: datetime

    class Config:
        from_attributes = True
