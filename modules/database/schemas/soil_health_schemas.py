from datetime import datetime

from pydantic import BaseModel


class SoilHealthBase(BaseModel):
    ph_level: float
    nitrogen_level: float
    phosphorus_level: float
    potassium_level: float
    organic_matter: float
    recommendations: str


class SoilHealthCreate(SoilHealthBase):
    farm_id: int


class SoilHealthInDB(SoilHealthBase):
    id: int
    farm_id: int
    analysis_date: datetime

    class Config:
        orm_mode = True
