from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FarmingAdviceBase(BaseModel):
    advice_type: str
    advice: str
    other_things_to_note: Optional[str] = None
    duration: Optional[str] = None

class FarmingAdviceCreate(FarmingAdviceBase):
    farm_id: int


class FarmingAdviceInDB(FarmingAdviceBase):
    id: int
    farm_id: int
    created_at: datetime

    class Config:
        from_attributes = True
