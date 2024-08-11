from datetime import datetime

from pydantic import BaseModel, Field


class CropDiagnosisBase(BaseModel):
    is_infected: bool
    crop_name: str
    crop_type: str
    disease_name: str
    treatment_recommendation: str
    how_to_identify_disease: str
    causes_of_disease: str
    other_things_to_note: str
    confidence_level: float
    images: list[str] = Field(default_factory=list)


class CropDiagnosisCreate(CropDiagnosisBase):
    crop_id: int


class CropDiagnosisInDB(CropDiagnosisBase):
    id: int
    crop_id: int
    created_at: datetime

    class Config:
        from_attributes = True
