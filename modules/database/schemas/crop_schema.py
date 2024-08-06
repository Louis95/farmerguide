from datetime import datetime

from pydantic import BaseModel


class CropBase(BaseModel):
    is_infected: bool
    crop_name: str
    notes: str
    planted_on: datetime
    harvested_on: datetime


class CropCreate(CropBase):
    farm_id: int


class CropInDB(CropBase):
    id: int
    farm_id: int
    created_at: datetime

    class Config:
        from_attributes = True
