from datetime import datetime

from pydantic import BaseModel


class FarmingAdviceBase(BaseModel):
    advice_type: str
    content: str


class FarmingAdviceCreate(FarmingAdviceBase):
    farm_id: int


class FarmingAdviceInDB(FarmingAdviceBase):
    id: int
    farm_id: int
    created_at: datetime

    class Config:
        orm_mode = True
